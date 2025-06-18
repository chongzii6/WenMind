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

def main(result1_path, result2_path):
    error = 0
    with open(result1_path, 'r', encoding='utf-8') as fin:
        data1 = json.load(fin)
    with open(result2_path, 'r', encoding='utf-8') as fin:
        data2 = json.load(fin)

    for i in tqdm(range(0, len(data1))):
        LLM_score_1 = data1[i]["LLM_score"]
        LLM_score_2 = data2[i]["LLM_score"]

        score_list1 = json.loads(LLM_score_1, strict=False)
        score_list2 = json.loads(LLM_score_2, strict=False)
        if score_list1 != score_list2:
            print(f"diff found in {i}, result1={score_list1}, result2={score_list2}")
            pass
        
if __name__ == "__main__":
    result1_path = os.path.join(PROJECT_DIR, "data", "qwen_turbo_06121502_result-score.json")
    result2_path = os.path.join(PROJECT_DIR, "data", "qwen_turbo_eval_06131847_result_fix_2.json")

    main(result1_path, result2_path)
