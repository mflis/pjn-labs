import json
import os
import re

root_dir = '/home/marcin/Desktop/SemestrVIII/PJN/lab1'
data_dir = f"{root_dir}/data/json"
tmp_path = f"{root_dir}/tmp/output1.txt"
json_files = os.listdir(data_dir)
judgements_files = filter(lambda name: re.match('judgments-\d+00\.json', name), json_files)
output_file = open(tmp_path, 'w')
# todo: only judgemntDate in 2018
for file in judgements_files:
    jsonFile = open(os.path.join(data_dir, file), 'r')
    judgements = json.load(jsonFile)['items']
    texts = map(lambda item: item['textContent'], judgements)
    output_file.write("".join(texts))
    jsonFile.close()

output_file.close()
