import json
import os
import re

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from constants import *


def prepare_json(judgement):
    return {
        'textContent': judgement['textContent'],
        'judgmentDate': judgement['judgmentDate'],
        'courtCases': judgement['courtCases'],
        'judges': judgement['judges']
    }


root_dir = '/home/marcin/Desktop/SemestrVIII/PJN/lab1'
json_data_dir = f"{root_dir}/data/json"
client = Elasticsearch()

json_files = os.listdir(json_data_dir)
judgements_2018 = list(filter(lambda name: re.match('judgments-(316[3-9]|317\d)\.json', name), json_files))

for filename in judgements_2018:
    with open(os.path.join(json_data_dir, filename), 'r') as jsonFile:
        judgements = json.load(jsonFile)['items']
    yearFiltered = filter(lambda item: "2018" in item['judgmentDate'], judgements)
    projected_objects = list(map(prepare_json, yearFiltered))
    bulk(client, projected_objects, index=index_name, doc_type='judgement')
