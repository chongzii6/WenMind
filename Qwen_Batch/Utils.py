import time
import os
import json

class Batch_Utils():
    def __init__(self, model, endpoint, system_prompt = None, top_p=0.8, temperature=0.7):
        self.BATCH_ENDPOINT = endpoint
        self.MODEL_NAME = model
        self.SYSTEM_PROMPT = system_prompt
        self.top_p = top_p
        self.temperature = temperature

    def __create_messages(self, prompt):
        msgs = [{"role":"user", "content": prompt }]
        if self.SYSTEM_PROMPT:
            msgs.append({"role": "system", "content": self.SYSTEM_PROMPT})
        return msgs

    def __create_body(self, prompt):
        obj = {
            "model": self.MODEL_NAME,
            "messages": self.__create_messages(prompt),
            "enable_thinking": "false",
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": 50, 
            "max_tokens": 2048,
            "seed": 100,
            "presence_penalty": 1.5,
        }
        return obj

    def create_line(self, id, query):
        obj = {
            "custom_id": id,
            "method":"POST",
            "url": self.BATCH_ENDPOINT,
            "body": self.__create_body(query)
        }
        return json.dumps(obj, ensure_ascii=False)

    def write_batch_index_file(self, lines, index, subdir, filename):
        filepath = os.path.join(subdir, filename + "_%d" % index) + ".jsonl"
        self.write_batch_file(lines, filepath)

    def write_batch_file(self, lines, filepath):
        with open(filepath, 'w', encoding='utf-8') as fout:
            for l in lines:
                fout.write(l+'\n')
