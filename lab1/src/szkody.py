import re

from filenames import *


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
    return re.compile(regex_pattern, re.IGNORECASE)


judgements_file = open(judgement_text_path, 'r')
results = 0
pattern = prepare_regex()

for line in judgements_file:
    results += bool(pattern.search(line))

print(f"nr of verdicts in 2018 with word `szkoda` or its variations are present: {results}")
