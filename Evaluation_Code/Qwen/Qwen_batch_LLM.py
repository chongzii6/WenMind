import os
import time

from pathlib import Path
from openai import OpenAI

class Qwen_batch_LLM():
    def __init__(self, endpoint):
        # 若没有配置环境变量,可用阿里云百炼API Key将下行替换为：api_key="sk-xxx",但不建议在生产环境中直接将API Key硬编码到代码中,以减少API Key泄露风险.
        API_KEY=os.getenv("DASHSCOPE_API_KEY")
        BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 阿里云百炼服务的base_url

        # 初始化客户端
        self.client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
        self.endpoint = endpoint

    def upload_file(self, file_path):
        print(f"正在上传包含请求信息的JSONL文件...")
        file_object = self.client.files.create(file=Path(file_path), purpose="batch")
        print(f"文件上传成功。得到文件ID: {file_object.id}\n")
        return file_object.id

    def create_batch_job(self, input_file_id):
        print(f"正在基于文件ID，创建Batch任务...")
        # 请注意:此处endpoint参数值需和输入文件中的url字段保持一致.测试模型(batch-test-model)填写/v1/chat/ds-test,Embedding文本向量模型填写/v1/embeddings,其他模型填写/v1/chat/completions
        batch = self.client.batches.create(input_file_id=input_file_id, endpoint=self.endpoint, completion_window="24h")
        print(f"Batch任务创建完成。 得到Batch任务ID: {batch.id}\n")
        return batch.id

    def check_job_status(self, batch_id):
        print(f"正在检查Batch任务状态...")
        batch = self.client.batches.retrieve(batch_id=batch_id)
        print(f"Batch任务状态: {batch.status}\n")
        return batch.status

    def get_output_id(self, batch_id):
        print(f"正在获取Batch任务中执行成功请求的输出文件ID...")
        batch = self.client.batches.retrieve(batch_id=batch_id)
        print(f"输出文件ID: {batch.output_file_id}\n")
        return batch.output_file_id

    def get_error_id(self, batch_id):
        print(f"正在获取Batch任务中执行错误请求的输出文件ID...")
        batch = self.client.batches.retrieve(batch_id=batch_id)
        print(f"错误文件ID: {batch.error_file_id}\n")
        return batch.error_file_id

    def download_results(self, output_file_id, output_file_path):
        print(f"正在打印并下载Batch任务的请求成功结果...")
        content = self.client.files.content(output_file_id)
        # 打印部分内容以供测试
        print(f"打印请求成功结果的前1000个字符内容: {content.text[:1000]}...\n")
        # 保存结果文件至本地
        content.write_to_file(output_file_path)
        print(f"完整的输出结果已保存至本地输出文件result.jsonl\n")

    def download_errors(self, error_file_id, error_file_path):
        print(f"正在打印并下载Batch任务的请求失败信息...")
        content = self.client.files.content(error_file_id)
        # 打印部分内容以供测试
        print(f"打印请求失败信息的前1000个字符内容: {content.text[:1000]}...\n")
        # 保存错误信息文件至本地
        content.write_to_file(error_file_path)
        print(f"完整的请求失败信息已保存至本地错误文件error.jsonl\n")

    def elapsed_time(self, start):
        elapsed_time = time.time() - start
        if elapsed_time < 60:
            return "%d sec" % elapsed_time
        else:
            min = int(elapsed_time / 60)
            sec = elapsed_time % 60
            if min < 60:
                return "%d:%02d" % (min, sec)
            else:
                hour = int(min / 60)
                min = min % 60
                return "%d:%02d:%02d" % (hour, min, sec)

    def process(self, input_file_path, output_file_path, error_file_path):
        try:
            # Step 1: 上传包含请求信息的JSONL文件,得到输入文件ID,如果您需要输入OSS文件,可将下行替换为：input_file_id = "实际的OSS文件URL或资源标识符"
            input_file_id = self.upload_file(input_file_path)

            # Step 2: 基于输入文件ID,创建Batch任务
            batch_id = self.create_batch_job(input_file_id)

            # Step 3: 检查Batch任务状态直到结束
            status = ""
            start_time = time.time()
            while status not in ["completed", "failed", "expired", "cancelled"]:
                status = self.check_job_status(batch_id)
                print(f"等待任务完成... Elapsed time: {self.elapsed_time(start_time)}")
                time.sleep(10)  # 等待10秒后再次查询状态
            # 如果任务失败,则打印错误信息并退出
            if status == "failed":
                batch = self.client.batches.retrieve(batch_id)
                print(f"Batch任务失败。错误信息为:{batch.errors}\n")
                print(f"参见错误码文档: https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
                return
            # Step 4: 下载结果：如果输出文件ID不为空,则打印请求成功结果的前1000个字符内容，并下载完整的请求成功结果到本地输出文件;
            # 如果错误文件ID不为空,则打印请求失败信息的前1000个字符内容,并下载完整的请求失败信息到本地错误文件.
            output_file_id = self.get_output_id(batch_id)
            if output_file_id:
                self.download_results(output_file_id, output_file_path)
            error_file_id = self.get_error_id(batch_id)
            if error_file_id:
                self.download_errors(error_file_id, error_file_path)
                print(f"参见错误码文档: https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        except Exception as e:
            print(f"An error occurred: {e}")
            print(f"参见错误码文档: https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
