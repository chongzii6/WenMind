from dotenv import load_dotenv
from tqdm import tqdm
from openai import OpenAI
from datetime import datetime
from pathlib import Path

import time
import os
import json

def gerenate(rawfile, resultfile, comparefile):
    answers = {}
    with open(resultfile, 'r', encoding='utf-8') as fin:
        for line in fin:
            json_obj = json.loads(line)
            custom_id = int(json_obj["custom_id"])
            body = json_obj['response']['body']
            # model = body['model']
            content = body['choices'][0]['message']['content']
            answers[custom_id] = content

    id = 0
    result = []
    with open(rawfile, 'r', encoding='utf-8') as fin:
        for line in fin:
            json_obj = json.loads(line)
            instruction = json_obj["instruction"]
            input = json_obj["input"]
            prompt = instruction + input
            output = json_obj["output"]
            
            obj = {
                "id": id,
                "question": prompt, 
                "answer": output,
                "llm_response": answers[id],
            }
            result.append(obj)
            id += 1

    with open(comparefile, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    load_dotenv()
    PROJECT_DIR = os.getcwd()

    rawfile = os.path.join(PROJECT_DIR, "COIG", "data", "trad-multi-choice-100.jsonl")
    resultfile = os.path.join(PROJECT_DIR, "COIG", "out", "trad-multi-choice-100.jsonl.result")
    comparefile = os.path.join(PROJECT_DIR, "COIG", "out", "trad-multi-choice-100.jsonl.compare")
    gerenate(rawfile, resultfile, comparefile)
