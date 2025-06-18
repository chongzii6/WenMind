from dotenv import load_dotenv
from tqdm import tqdm
from openai import OpenAI
from datetime import datetime
from pathlib import Path

import time
import os
import json
import sys
sys.path.append(os.getcwd())
print(f"sys.path={sys.path}")

from Qwen_Batch.Executor import LLM_Executor
from Qwen_Batch.Utils import Batch_Utils

# Load environment variables from .env file
# LLM_scoring_prompts_filepath = os.path.join(PROJECT_DIR, "JSON", "Task_Score_Prompt.json")
# MODEL_NAME = os.getenv('MODEL_NAME')
MODEL_NAME = 'qwen-turbo'
BATCH_ENDPOINT = "/v1/chat/completions"

def generate(infile, test_batch_file):
    batch_lines = []
    maker = Batch_Utils(MODEL_NAME, BATCH_ENDPOINT)
    id = 0
    with open(infile, 'r', encoding='utf-8') as fin:
        for line in fin:
            json_obj = json.loads(line)
            instruction = json_obj["instruction"]
            input = json_obj["input"]
            prompt = instruction + input

            newline = maker.create_line(id, prompt)
            batch_lines.append(newline)

            id += 1
            output = json_obj["output"]

    maker.write_batch_file(batch_lines, test_batch_file)

def execute_batch(test_batch_file, outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    llm = LLM_Executor(BATCH_ENDPOINT)
    paths = os.path.split(test_batch_file)
    res = os.path.join(outdir, paths[1] + ".result")
    err = os.path.join(outdir, paths[1] + ".error")
    # print(fp)

    llm.process(test_batch_file, res, err)

if __name__ == "__main__":
    load_dotenv()
    PROJECT_DIR = os.getcwd()

    infile = os.path.join(PROJECT_DIR, "COIG", "data", "trad-multi-choice-100.jsonl")
    test_batch_file = os.path.join(PROJECT_DIR, "COIG", "test", "trad-multi-choice-100.jsonl")

    # generate(infile, test_batch_file)

    outdir = os.path.join(PROJECT_DIR, "COIG", "out")
    execute_batch(test_batch_file, outdir)