import re

import matplotlib.pyplot as plt
import numpy as np

from filenames import *


# uwzględnić PLN
# ignore case
def clean_number(num_str):
    return num_str.replace(" ", "").replace(".", "").replace(",", "")


def normalize_match(number, decimal, magnitude):
    float_str = clean_number(number)
    decimal_str = "." + (decimal or "0")

    float_number = int(float_str)
    decimal_number = float(decimal_str)
    magnitude_map = {
        None: 1.0,
        'tys': 1000.0,
        'mln': 1000000.0,
        'mil': 1000000.0,
        'mld': 1000000000.0,
    }
    return (float_number + decimal_number) * magnitude_map[magnitude]


def prepare_regex():
    magnitude_shortcuts = "(?P<magnitude>(tys|mln|mld|mil))"
    magnitudes = f"({magnitude_shortcuts}\.?)?"
    number = "(?P<number>([. ]*\d+)+)"
    decimal_part = "(,(?P<decimal>\d+))?"
    old = "(\(?\s*starych\s*\)?)?"
    numbers_as_words = "(\(.*\))?"
    pln = "(zł|PLN)"
    combined = f"{number}{decimal_part}\s*{magnitudes}\s*{old}{numbers_as_words}\s*{pln}"
    return re.compile(combined, re.IGNORECASE)


def process_file(judgements_file):
    results = []
    pattern = prepare_regex()

    for line in judgements_file:
        process_line(line, pattern, results)

    return results


def process_line(line, pattern, results):
    for match_result in pattern.finditer(line):
        numeric_match = match_result.group('number')
        magnitude_match = match_result.group('magnitude')
        decimal_match = match_result.group('decimal')
        float_nr = normalize_match(numeric_match, decimal_match, magnitude_match)
        if float_nr > 0.01:  # filer out 0 zł
            results.append(float_nr)

    return results


def create_histogram(data, output_filename):
    logbins = np.geomspace(data.min(), data.max(), 40)
    plt.hist(data, bins=logbins, rwidth=0.9)
    plt.xscale('log')
    plt.xlabel("Amount of money [zł]")
    plt.ylabel("Nr of occurences")
    plt.savefig(output_filename)
    plt.close()


output_file = open(judgement_text_path, 'r')

money_amounts = np.asarray(process_file(output_file))
lesser_amounts = money_amounts[money_amounts < 1000000]
bigger_amounts = money_amounts[money_amounts >= 1000000]

create_histogram(money_amounts, '../plots/amounts-all.png')
create_histogram(lesser_amounts, '../plots/amounts-lesser.png')
create_histogram(bigger_amounts, '../plots/amounts-bigger.png')
