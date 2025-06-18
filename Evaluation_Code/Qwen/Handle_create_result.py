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



# for i,_ in enumerate(tqdm(data_test)):
#     query = data_test[i]["question"]
#     response = use_model(query)

#     data_test[i]["LLM_name"] = "Qwen1.5-7B-Chat"
#     data_test[i]["LLM_response"] = response
#     save_answer.append(data_test[i])

#     with open(args.output_path, "w", encoding="utf-8") as f:
#         json.dump(save_answer, f, ensure_ascii=False, indent=2)



def main(result_dir, output_path):
    with open(LLM_BENCHMARK_filepath, 'r', encoding='utf-8') as fin:
        data_test = json.load(fin)

    save_answer = []
    for file in os.listdir(result_dir):
        fp = os.path.join(result_dir, file)

        if os.path.isfile(fp):
            print(fp)

            with open(fp, 'r', encoding='utf-8') as f:
                for line in f:
                    data_result = json.loads(line)
                    id = int(data_result['custom_id'])
                    body = data_result['response']['body']
                    model = body['model']
                    content = body['choices'][0]['message']['content']
                    data_test[id]["LLM_name"] = model
                    data_test[id]["LLM_response"] = content
                    save_answer.append(data_test[id])
                    # print(len(data_result))

                # data_test[i]["LLM_name"] = "Qwen1.5-7B-Chat"
                # data_test[i]["LLM_response"] = response
                # save_answer.append(data_test[i])

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(save_answer, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    use_dir = os.path.join(PROJECT_DIR, "data", "batch_06121502_result")
    output_path = os.path.join(PROJECT_DIR, "data", "qwen_turbo_06121502_result.json")
    main(result_dir = use_dir, output_path = output_path)
