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

def main(eval_result_path, good_result_path):
    good_result = []
    error = 0
    with open(eval_result_path, 'r', encoding='utf-8') as fin:
        data = json.load(fin)

        for d in data:
            LLM_score = d["LLM_score"]
            try:
                score_list = json.loads(LLM_score, strict=False)
                good_result.append(d)
            except json.JSONDecodeError as e:
                error += 1
                print(f"found JSONDecodeError {e} at {d["id"]}")
                if e.msg.startswith('Unterminated string starting at'):
                    d["LLM_score"] = LLM_score[:-2] + '"' + LLM_score[-1:]
                    good_result.append(d)
                elif e.msg.startswith("Expecting ',' delimiter"):
                    pos = e.pos-1
                    d["LLM_score"] = LLM_score[:pos] + LLM_score[pos:-2].replace('"', '“') + LLM_score[-2:]
                    good_result.append(d)
                elif e.msg.startswith("Extra data"):
                    d["LLM_score"] = LLM_score[:-1]
                    good_result.append(d)
                else:
                    print(f"JSONDecodeError {e} at {d["id"]}")
            except Exception as e:
                print(f"发生了一个未知错误: {e} at {d["id"]}")

    print(f"fix {error} error")
    with open(good_result_path, "w", encoding="utf-8") as f:
        json.dump(good_result, f, ensure_ascii=False, indent=2)
        print(f"corrected eval score saved to: {good_result_path}")

if __name__ == "__main__":
    eval_result_path = os.path.join(PROJECT_DIR, "data", "qwen_turbo_eval_06131847_result_fix_1.json")
    good_result_path = os.path.join(PROJECT_DIR, "data", "qwen_turbo_eval_06131847_result_fix_2.json")

    main(eval_result_path, good_result_path)
