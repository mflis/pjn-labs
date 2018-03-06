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
    pln = "(zł)"
    combined = f"{number}{decimal_part}\s*{magnitudes}\s*{old}{numbers_as_words}\s*{pln}"
    return re.compile(combined)


def process_file(judgements_file):
    results = []
    pattern = prepare_regex()

    for line in judgements_file:
        res = pattern.search(line)
        if res is not None:
            numeric_match = res.group('number')
            magnitude_match = res.group('magnitude')
            decimal_match = res.group('decimal')
            float_nr = normalize_match(numeric_match, decimal_match, magnitude_match)
            if float_nr > 0.01:
                results.append(float_nr)

    return results


output_file = open(judgement_text_path, 'r')
money_amounts = np.asarray(process_file(output_file))
logbins = np.geomspace(money_amounts.min(), money_amounts.max(), 15)

plt.hist(money_amounts, bins=logbins)
plt.xscale('log')
plt.title("Kwoty w wyrokach sądowych 2018")
plt.xlabel("kwota [zł]")
plt.ylabel("Częstotliwość")
plt.savefig('kwoty-all.png')
plt.close()
lesser_amounts = money_amounts[money_amounts < 1000000]
logbins_lesser = np.geomspace(lesser_amounts.min(), lesser_amounts.max(), 15)

bigger_amounts = money_amounts[money_amounts >= 1000000]
logbins_bigger = np.geomspace(bigger_amounts.min(), bigger_amounts.max(), 15)

plt.hist(lesser_amounts, bins=logbins_lesser)
plt.xscale('log')
plt.title("Kwoty w wyrokach sądowych 2018 mniejsze niż 1 mln zł")
plt.xlabel("kwota [zł]")
plt.ylabel("Częstotliwość")
plt.savefig('kwoty-lesser.png')
plt.close()

plt.hist(bigger_amounts, bins=logbins_bigger)
plt.xscale('log')
plt.title("Kwoty w wyrokach sądowych 2018 większe niż 1 mln zł")
plt.xlabel("kwota [zł]")
plt.ylabel("Częstotliwość")
plt.savefig('kwoty-bigger.png')
plt.close()
