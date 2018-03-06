import itertools
import json
import os
import re

from filenames import *

json_files = os.listdir(json_data_dir)
judgements_2018 = list(filter(lambda name: re.match('judgments-(316[3-9]|317\d)\.json', name), json_files))
verdict_file = open(judgement_text_path, 'w')
regulations_text_file = open(referenced_regulations_text_path, 'w')
art445Pattern = re.compile("art\.\s*445", re.IGNORECASE)


def is_referencing_regulation(ref_entry):
    return ref_entry['journalYear'] == 1964 \
           and ref_entry['journalNo'] == 16 \
           and ref_entry['journalEntry'] == 93


def referenced_regulations_processing(judgements_array):
    regulations = map(lambda item: item['referencedRegulations'], judgements_array)
    regulations_flat = itertools.chain.from_iterable(regulations)
    mentioned_regulation = filter(is_referencing_regulation, regulations_flat)
    regulations_text = map(lambda item: item['text'], mentioned_regulation)
    return list(filter(lambda text: bool(art445Pattern.search(text)), regulations_text))


def append_array_to_file(file, arr):
    stripped = map(lambda line: line.replace("\n", ""), arr)
    file.write("\n".join(stripped))
    file.write("\n")


mentioned = 0
for filename in judgements_2018:
    with open(os.path.join(json_data_dir, filename), 'r') as jsonFile:
        judgements = json.load(jsonFile)['items']
    yearFiltered = list(filter(lambda item: "2018" in item['judgmentDate'], judgements))
    mentioning_article = referenced_regulations_processing(judgements)
    verdicts = map(lambda item: item['textContent'], yearFiltered)
    append_array_to_file(verdict_file, verdicts)
    append_array_to_file(regulations_text_file, mentioning_article)
    mentioned += len(mentioning_article)

print(f"art. 445 was mentioned  in {mentioned} verdicts in 2018")
verdict_file.close()
regulations_text_file.close()
