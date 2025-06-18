import requests
import json
from tqdm import tqdm
from openai import OpenAI
import os

template = '''{"custom_id":"%d","method":"POST","url":"/v1/chat/completions","body":{"model":"%s","messages":[{"role":"user","content":"%s"}],"enable_thinking":"false"}}\n'''

# {"custom_id":"1","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen-turbo-latest","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"你好！有什么可以帮助你的吗？"}]}}
# {"custom_id":"2","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen-turbo-latest","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"What is 2+2?"}]}}

LLM_scoring_prompts_file = os.path.join(os.getcwd(), "JSON", "Task_Score_Prompt.json")
model = "qwen-turbo"    #no-thinking
# model = "qwen-turbo-latest"   #thinking

def create_batch(infile, outfile, promtfile):
    print(f"input={infile}, output={outfile}, prompt={promtfile}\nusing model={model}")

    with open(infile, 'r', encoding='utf-8') as file:
        data = json.load(file)

    with open(promtfile, 'r', encoding='utf-8') as file:
        prompt_list = json.load(file)

    multi_choice = [3627,3630,3632,3633,3635,3637,3643,3646,3650,3666,3671,3672,3674]

    with open(outfile, "w", encoding="utf-8") as fout:
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

            # line = template % (i, model, input)
            obj = {
                "custom_id": "%d" % i,
                "method":"POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model":"%s" % model,
                    "messages": [{"role":"user", "content": "%s" % input }],
                    "enable_thinking": "false"
                }
            }
            line = json.dumps(obj, ensure_ascii=False)
            # print(line)
            fout.write(line + '\n')

def _showhelp():
    print(f'''{os.path.basename(argv[0])} [options] <input response file>\nOption: \n\t-h --help: show help \n\t-o <file> --out=<file>: output intermediate batch file\n\t-p <file> \
--prompt=<file>: scoring promts file, default = {LLM_scoring_prompts_file}\n''')

if __name__ == '__main__':
    from sys import argv
    import getopt

    # LLM_input_response_file = "..\data\Qwen3-8B-nt.json")
    # LLM_output_score_file = "..\data\LLM_score.json"

    opts, args = getopt.getopt(argv[1:],'-h-o:-p:',['help','out=','prompt='])
    for opt_name, opt_value in opts:
        if opt_name in ('-h','--help'):
            _showhelp()
            exit()
        if opt_name in ('-o','--out'):
            LLM_output_batch_file = opt_value
        if opt_name in ('-p','--prompt'):
            LLM_scoring_prompts_file = opt_value

    print(f"cwd={os.getcwd()}")
    if len(args) > 0 and LLM_output_batch_file:
        LLM_input_response_file = args[0]
        if os.path.exists(LLM_input_response_file) and os.path.exists(LLM_scoring_prompts_file):
            create_batch(LLM_input_response_file, LLM_output_batch_file, LLM_scoring_prompts_file)
            exit()

    _showhelp()
