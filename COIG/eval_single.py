from dotenv import load_dotenv
from tqdm import tqdm
from openai import OpenAI
from datetime import datetime
from pathlib import Path

import time
import os
import json

MODEL_NAME = 'qwen2.5-7b-instruct'

def call_llm(llm, all_prompt):
    completion = llm.chat.completions.create(
        # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": all_prompt},
        ],
        # Qwen3模型通过enable_thinking参数控制思考过程（开源版默认True，商业版默认False）
        # 使用Qwen3开源版模型时，若未启用流式输出，请将下行取消注释，否则会报错
        extra_body={"enable_thinking": False},
    )

    response_text = completion.choices[0].message.content
    return response_text

def generate(llm, infile, resultfile):
    result = []

    with open(infile, 'r', encoding='utf-8') as fin:
        lines = fin.readlines()
        for id, line in enumerate(tqdm(lines, desc='Reading file')):
            json_obj = json.loads(line)
            instruction = json_obj["instruction"]
            input = json_obj["input"]
            prompt = instruction + input
            output = json_obj["output"]

            response = call_llm(llm, prompt)
            obj = {
                "id": id,
                "question": prompt, 
                "answer": output,
                "llm_response": response,
            }
            result.append(obj)

    with open(resultfile, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    load_dotenv()
    PROJECT_DIR = os.getcwd()

    infile = os.path.join(PROJECT_DIR, "COIG", "data", "trad-multi-choice-100.jsonl")
    # resultfile = os.path.join(PROJECT_DIR, "COIG", "out", "trad-multi-choice-100.jsonl.llm_answer")
    resultfile = os.path.join(PROJECT_DIR, "COIG", "out", "trad-multi-choice-100.jsonl.llm_answer.0")

    llm = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    generate(llm, infile, resultfile)