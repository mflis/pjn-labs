import json
import pandas
import os
import re
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

from constants import *


def count_words():
    all_text = ""
    json_files = os.listdir(json_data_dir)
    judgements_in_year = list(filter(lambda name: re.match(filesInYearPattern, name), json_files))
    for filename in judgements_in_year:
        with open(os.path.join(json_data_dir, filename), 'r') as jsonFile:
            judgements = json.load(jsonFile)['items']
        year_filtered = filter(lambda item: year in item['judgmentDate'], judgements)
        texts = map(lambda item: item['textContent'], year_filtered)
        joined = " ".join(texts)
        notags = re.sub(r"<[^>]*>", " ", joined)
        nobreaks = re.sub(r"-\n", " ", notags)
        nodigits = re.sub(r"\d+", " ", nobreaks)
        noroman = re.sub(r"\b[XVILMC]+\b", "", nodigits)
        lower = noroman.lower()
        all_text += lower
    return Counter(re.findall(r'\w{2,}', all_text))


def save_frequencies(counter: Counter):
    with open('list.txt', 'w') as file:
        frequencies = counter.most_common()
        words = map(lambda x: x[0] + '\n', frequencies)
        file.writelines(words)


def plot_histogram(counter: Counter):
    labels, values = zip(*count_words().most_common(barplot_nr_of_items))
    indexes = np.arange(len(labels))
    plt.bar(indexes, values, log=True)
    plt.xticks(indexes, labels, rotation='vertical', fontsize=1)
    plt.savefig('../frequencies.png')


def load_polimorfologik():
    pd = pandas.read_csv('polimorfologik-2.1.txt', usecols=[1])
    set()


counted = count_words()
save_frequencies(counted)
plot_histogram(counted)
