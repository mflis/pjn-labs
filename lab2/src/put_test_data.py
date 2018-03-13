from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from constants import *


def prepare_json(judgement):
    return {
        'textContent': judgement,
        'judgmentDate': '2018-03-10',
        'courtCases': {

            'caseNumber': 'sdsfc'

        },
        'judges': {

            'name': 'scsc'

        }
    }


uszczerb_file = '/home/marcin/Desktop/SemestrVIII/PJN/lab2/test_data.txt'
client = Elasticsearch()
with open(uszczerb_file, 'r') as lineFile:
    projected_objects = []
    for line in lineFile:
        projected_object = prepare_json(line)
        projected_objects.append(projected_object)

bulk(client, projected_objects, index=index_name, doc_type='judgement')
