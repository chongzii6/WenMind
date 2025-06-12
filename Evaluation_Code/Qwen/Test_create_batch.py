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
LLM_BENCHMARK_filepath = os.path.join(PROJECT_DIR, "WenMind_Benchmark", "WenMind_ver1.json")
LLM_TEST_file = "test_batch"

# chat_model.generation_config.max_new_tokens = 2048
# chat_model.generation_config.temperature = 1.0
# chat_model.generation_config.top_p = 1
# chat_model.generation_config.top_k = 50
# chat_model.generation_config.repetition_penalty = 1.0
# chat_model.generation_config.do_sample = False

#     messages = [
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": prompt}
#     ]

TEST = False
# MODEL_NAME = "batch-test-model"
# BATCH_ENDPOINT = "/v1/chat/ds-test"
MODEL_NAME = os.getenv('MODEL_NAME')
BATCH_ENDPOINT = "/v1/chat/completions"

def create_body(prompt):
    obj = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
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
    filepath = os.path.join(subdir, LLM_TEST_file + "_%d" % index) + ".jsonl"
    with open(filepath, 'w', encoding='utf-8') as fout:
        for l in batch:
            fout.write(l+'\n')

def create_batch_files(subdir, max_line = 1000, test_only = False):
    if test_only:
        max_line = 20

    with open(LLM_BENCHMARK_filepath, 'r', encoding='utf-8') as fin:
        data_test = json.load(fin)

    batch = []
    index = 0

    for i,_ in enumerate(tqdm(data_test)):
        query = data_test[i]["question"]
        id = str(data_test[i]["id"])
        line = create_line(id, query)
        batch.append(line)

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

def main(use_dir = None, create_file_only = False):
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
        create_batch_files(subdir, test_only = TEST)

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
    use_dir = os.path.join(PROJECT_DIR, "data", "batch_06121502_0")
    main(use_dir = use_dir)