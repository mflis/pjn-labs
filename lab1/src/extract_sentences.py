import json
import os
import re

from filenames import *

json_files = os.listdir(json_data_dir)
judgements_files = filter(lambda name: re.match('judgments-\d+00\.json', name), json_files)
output_file = open(judgement_text_path, 'w')
# todo: only judgemntDate in 2018
for file in judgements_files:
    jsonFile = open(os.path.join(json_data_dir, file), 'r')
    judgements = json.load(jsonFile)['items']
    texts = map(lambda item: item['textContent'], judgements)
    output_file.write("".join(texts))
    jsonFile.close()

output_file.close()
