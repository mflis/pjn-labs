import re

from filenames import *


# uwzględnić PLN
# ignore case


def prepare_regex():
    word_forms = [
        'szkoda',
        'szkody',
        'szkodzie',
        'szkodę',
        'szkodą',
        'szkodzie',
        'szkodo',
        "szkody",
        "szkód",
        "szkodom",
        "szkody",
        "szkody",
        "szkodach",
        "szkody",
    ]
    regex_pattern = f"({'|'.join(word_forms)})"
    return re.compile(regex_pattern)


def process_file(judgements_file):
    results = 0
    pattern = prepare_regex()

    for line in judgements_file:
        results += bool(pattern.search(line))

    return results


output_file = open(judgement_text_path, 'r')
print(process_file(output_file))
# najpierw zdefinowac skrtukture indeksu potem zaladowac dane, żeby dobrze zadizałałał
