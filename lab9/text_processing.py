import json
import os
import re
from itertools import chain
from operator import itemgetter

root_dir = '/home/marcin/Desktop/SemestrVIII/PJN'
year = "2017"
json_data_dir = f"{root_dir}/data/json"


def extract_file_number(filename):
    return int(filename.split('-')[1].split('.')[0])


def is_2017_in_file(filename):
    return 2716 <= extract_file_number(filename) <= 3163


def is_2018_in_file(filename):
    return 3163 <= extract_file_number(filename) <= 3173


def clean_text(line):
    notags = re.sub(r"<[^>]*>", " ", line)
    nobreaks = re.sub(r"-\n", "", notags)
    single_line = re.sub(r"\n", " ", nobreaks)
    single_space = re.sub(r"\s+", " ", single_line)
    noparens = single_space.replace("(...)", "")
    lower = noparens.lower()
    return lower + "\n"


def judgements_raw(filename):
    with open(os.path.join(json_data_dir, filename), 'r') as jsonFile:
        judgements = json.load(jsonFile)['items']
    return judgements


def prepare_raw_text(file_selector):
    judgements_files = filter(file_selector, os.listdir(json_data_dir))
    texts = chain.from_iterable(map(judgements_raw, judgements_files))
    return map(lambda judgement: clean_text(judgement['textContent']), texts)
