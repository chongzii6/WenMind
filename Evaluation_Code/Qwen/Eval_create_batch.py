from dotenv import load_dotenv
from tqdm import tqdm
from openai import OpenAI
from datetime import datetime
from pathlib import Path

import time
import os
import json

# Load environment variables from .env file
load_dotenv()

PROJECT_DIR = os.getcwd()
LLM_scoring_prompts_filepath = os.path.join(PROJECT_DIR, "JSON", "Task_Score_Prompt.json")
# LLM_BENCHMARK_filepath = os.path.join(PROJECT_DIR, "WenMind_Benchmark", "WenMind_ver1.json")
LLM_Batch_Eval_file = "eval_batch"

MODEL_NAME = os.getenv('MODEL_NAME')
MODEL_NAME = 'qwen-plus'
BATCH_ENDPOINT = "/v1/chat/completions"

def create_body(prompt):
    obj = {
        "model": MODEL_NAME,
        "messages": [
            {"role":"user", "content": prompt }
        ],
        "enable_thinking": "false",
        "temperature": 1.0,
        "top_p": 1,
        "top_k": 50, 
        "max_tokens": 2048,
        "seed": 100,
        "presence_penalty": 1.5,
    }
    return obj

def create_line(id, query):
    obj = {
        "custom_id": id,
        "method":"POST",
        "url": BATCH_ENDPOINT,
        "body": create_body(query)
    }
    return json.dumps(obj, ensure_ascii=False)

def write_batch_file(batch, index, subdir):
    filepath = os.path.join(subdir, LLM_Batch_Eval_file + "_%d" % index) + ".jsonl"
    with open(filepath, 'w', encoding='utf-8') as fout:
        for l in batch:
            fout.write(l+'\n')


def create_batch_files(test_response, subdir, max_line = 1000, test_only = False):
    with open(test_response, 'r', encoding='utf-8') as file:
        data = json.load(file)

    with open(LLM_scoring_prompts_filepath, 'r', encoding='utf-8') as file:
        prompt_list = json.load(file)

    batch = []
    index = 0
    multi_choice = [3627,3630,3632,3633,3635,3637,3643,3646,3650,3666,3671,3672,3674]

    for i in tqdm(range(0,len(data))):
        if data[i]["coarse_grained_task_zh"] == "文言文写作":
            input = prompt_list[7]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "七言律诗" in data[i]["question"]:
            input = prompt_list[8]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "五言律诗" in data[i]["question"]:
            input = prompt_list[9]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "七言绝句" in data[i]["question"]:
            input = prompt_list[10]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "五言绝句" in data[i]["question"]:
            input = prompt_list[11]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "七言排律" in data[i]["question"]:
            input = prompt_list[12]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "五言排律" in data[i]["question"]:
            input = prompt_list[13]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "念奴娇" in data[i]["question"]:
            input = prompt_list[14]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "满江红" in data[i]["question"]:
            input = prompt_list[15]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "虞美人" in data[i]["question"]:
            input = prompt_list[16]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "浣溪沙" in data[i]["question"]:
            input = prompt_list[17]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "菩萨蛮" in data[i]["question"]:
            input = prompt_list[18]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "水调歌头" in data[i]["question"]:
            input = prompt_list[19]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "卜算子" in data[i]["question"]:
            input = prompt_list[20]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "如梦令" in data[i]["question"]:
            input = prompt_list[21]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "渔家傲" in data[i]["question"]:
            input = prompt_list[22]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "西江月" in data[i]["question"]:
            input = prompt_list[23]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "天净沙" in data[i]["question"]:
            input = prompt_list[24]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "山坡羊" in data[i]["question"]:
            input = prompt_list[25]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "湘妃怨" in data[i]["question"]:
            input = prompt_list[26]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "古诗词创作" and "清江引" in data[i]["question"]:
            input = prompt_list[27]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "对联" and data[i]["fine_grained_task_zh"] == "接下联":
            input = prompt_list[4]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "对联" and data[i]["fine_grained_task_zh"] == "对联创作":
            input = prompt_list[5]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "对联" and data[i]["fine_grained_task_zh"] == "拟横批":
            input = prompt_list[6]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["coarse_grained_task_zh"] == "成语" and data[i]["fine_grained_task_zh"] == "近义词":
            input = prompt_list[3]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        elif data[i]["question_format"] == "MCQ" and data[i]["id"] in multi_choice:
            input = prompt_list[1]["prompt"].format(data[i]["LLM_response"],data[i]["answer"])
        elif data[i]["question_format"] == "MCQ" and data[i]["id"] not in multi_choice and data[i]["coarse_grained_task_zh"] != "情感分类":
            input = prompt_list[0]["prompt"].format(data[i]["LLM_response"],data[i]["answer"])
        elif data[i]["coarse_grained_task_zh"] == "情感分类":
            input = prompt_list[2]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])
        else:
            input = prompt_list[2]["prompt"].format(data[i]["LLM_response"],data[i]["answer"],data[i]["question"])      

        id = str(data[i]["id"])
        line = create_line(id, input)
        batch.append(line)

        # response_json = json.loads(main_use(input))
        # response_text = response_json["result"]
        # data[i]["LLM_score"] = response_text
        # all_list.append(data[i])

        if i % max_line == max_line-1:
            if test_only:
                break
            else:
                write_batch_file(batch, index, subdir)
                batch = []
                index += 1

    if len(batch) > 0:
        write_batch_file(batch, index, subdir)

from Qwen_batch_LLM import Qwen_batch_LLM

def main(test_resp, use_dir = None, create_file_only = False):
    if use_dir and os.path.exists(use_dir):
        subdir = use_dir
        create_files = False
    else:
        formatted_date = datetime.now().strftime("%m%d%H%M")
        subdir = os.path.join(PROJECT_DIR, "data", "batch_" + formatted_date)
        create_files = True

    resdir = os.path.join(subdir, "result")
    if not os.path.exists(resdir):
        os.makedirs(resdir)

    if create_files:
        create_batch_files(test_resp, subdir, max_line=2000, test_only = False)

    if create_file_only:
        return

    llm = Qwen_batch_LLM(BATCH_ENDPOINT)
    for file in os.listdir(subdir):
        fp = os.path.join(subdir, file)

        if os.path.isfile(fp):
            res = os.path.join(resdir, file + ".result")
            err = os.path.join(resdir, file + ".error")
            print(fp)

            llm.process(fp, res, err)


if __name__ == "__main__":
    use_dir = os.path.join(PROJECT_DIR, "data", "batch_06131847_1")
    # use_dir = None
    test_resp = os.path.join(PROJECT_DIR, "data", "qwen_turbo_06121502_result.json")
    main(test_resp, use_dir, create_file_only=False)
