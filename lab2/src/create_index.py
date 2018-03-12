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


create_index_body = {
    'settings': {
        # just one shard, no replicas for testing
        'number_of_shards': 1,
        'number_of_replicas': 0,

        'analysis': {
            'analyzer': {
                'polish': {
                    'type': 'custom',
                    'tokenizer': 'standard',
                    'filter': ["morfologik_stem"],
                }
            }
        }
    },
    'mappings': {
        'judgement': {
            'properties': {
                'textContent': {'type': 'text', 'analyzer': 'polish'},
                'judgmentDate': {'type': 'date'},
                'courtCases.caseNumber': {'type': 'keyword'},
                'judges.name': {'type': 'keyword'}
            }
        }
    }
}

es = Elasticsearch()
es.indices.delete(index=index_name, ignore=[400, 404])
es.indices.create(index=index_name, body=create_index_body)

client = Elasticsearch()

json_files = os.listdir(json_data_dir)
judgements_2018 = list(filter(lambda name: re.match(filesInYearPattern, name), json_files))

for filename in judgements_2018:
    with open(os.path.join(json_data_dir, filename), 'r') as jsonFile:
        judgements = json.load(jsonFile)['items']
    yearFiltered = filter(lambda item: "2018" in item['judgmentDate'], judgements)
    projected_objects = list(map(prepare_json, yearFiltered))
    bulk(client, projected_objects, index=index_name, doc_type='judgement')
