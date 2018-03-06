import itertools
import json
import os
import re

from filenames import *

json_files = os.listdir(json_data_dir)
judgements_files = list(filter(lambda name: re.match('judgments-(316[3-9]|317\d)\.json', name), json_files))
verdict_file = open(judgement_text_path, 'w')
regulations_text_file = open(referenced_regulations_text_path, 'w')
regulations_text_file_raw = open(referenced_regulations_text_path + 'raw', 'w')
artPattern = re.compile("art\.\s*445")


def isReferencingRegulation(refEntry):
    return refEntry['journalYear'] == 1964 and refEntry['journalNo'] == 16 and refEntry['journalEntry'] == 93


def referenced_regulations_processing(judgements_arr):
    regulations = list(map(lambda item: item['referencedRegulations'], judgements_arr))
    regulations_flat = list(itertools.chain.from_iterable(regulations))
    mentioned_regulation = list(filter(isReferencingRegulation, regulations_flat))
    regulations_text = list(map(lambda item: item['text'], mentioned_regulation))
    return list(filter(lambda text: bool(artPattern.search(text)), regulations_text)), regulations_text


mentioned = 0
for file in judgements_files:
    with open(os.path.join(json_data_dir, file), 'r') as jsonFile:
        judgements = json.load(jsonFile)['items']
    yearFiltered = list(filter(lambda item: "2018" in item['judgmentDate'], judgements))
    mentioning_article, mentioning_raw = referenced_regulations_processing(judgements)
    verdicts = list(map(lambda item: item['textContent'].replace("\n", ""), yearFiltered))
    verdict_file.write("\n".join(verdicts))
    verdict_file.write("\n")
    mentioned += len(mentioning_article)
    regulations_text_file.write("\n".join(mentioning_article))
    regulations_text_file.write("\n")

print(mentioned)
verdict_file.close()
regulations_text_file.close()
