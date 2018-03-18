import json
import os
import re
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

from constants import *

json_files = os.listdir(json_data_dir)
judgements_in_year = list(filter(lambda name: re.match(filesInYearPattern, name), json_files))

counters = []
all_text = ""
for filename in judgements_in_year:
    with open(os.path.join(json_data_dir, filename), 'r') as jsonFile:
        judgements = json.load(jsonFile)['items']
    yearFiltered = filter(lambda item: "2018" in item['judgmentDate'], judgements)
    texts = map(lambda item: item['textContent'], yearFiltered)
    joined = " ".join(texts)
    notags = re.sub(r"<[^>]*>", " ", joined)
    nobreaks = re.sub(r"-\n", " ", notags)
    nodigits = re.sub(r"\d+", " ", nobreaks)
    noroman = re.sub(r"\b[XVILMC]+\b", "", nodigits)
    lower = noroman.lower()
    all_text += lower
counted = Counter(re.findall(r'\w{2,}', all_text))
labels, values = zip(*counted.most_common(barplot_nr_of_items))
indexes = np.arange(len(labels))
plt.bar(indexes, values, log=True)
plt.xticks(indexes, labels, rotation='vertical', fontsize=1)
plt.savefig('../frequencies.png')
