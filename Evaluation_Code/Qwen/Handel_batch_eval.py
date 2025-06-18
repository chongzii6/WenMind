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
LLM_BENCHMARK_filepath = os.path.join(PROJECT_DIR, "WenMind_Benchmark", "WenMind_ver1.json")

def main(test_resp, result_dir, output_path):
    Max_id = 4874 + 1
    data_test = [0] * Max_id
    with open(test_resp, 'r', encoding='utf-8') as fin:
        data = json.load(fin)
        for d in data:
            id = d['id']
            data_test[id] = d

    #check data_test
    for i in range(Max_id):
        if data_test[i] == 0:
            print(f"lack response in {i}")

    save_eval = []
    for file in os.listdir(result_dir):
        fp = os.path.join(result_dir, file)

        if os.path.isfile(fp):
            print(fp)

            with open(fp, 'r', encoding='utf-8') as f:
                for line in f:
                    data_result = json.loads(line)
                    id = int(data_result['custom_id'])
                    body = data_result['response']['body']
                    # model = body['model']
                    content = body['choices'][0]['message']['content']
                    # data_test[id]["LLM_name"] = model
                    data_test[id]["LLM_score"] = content
                    save_eval.append(data_test[id])
                    # print(len(data_result))

                # data_test[i]["LLM_name"] = "Qwen1.5-7B-Chat"
                # data_test[i]["LLM_response"] = response
                # save_answer.append(data_test[i])

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(save_eval, f, ensure_ascii=False, indent=2)
        print(f"eval score saved to: {output_path}")

if __name__ == "__main__":
    use_dir = os.path.join(PROJECT_DIR, "data", "batch_06131847_result")
    output_path = os.path.join(PROJECT_DIR, "data", "qwen_turbo_eval_06131847_result.json")
    test_resp = os.path.join(PROJECT_DIR, "data", "qwen_turbo_06121502_result.json")

    main(test_resp, result_dir = use_dir, output_path = output_path)
