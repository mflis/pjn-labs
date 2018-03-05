import re


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
    number = "(?P<number>([. ]?\d+)+)"
    decimal_part = "(,(?P<decimal>\d+))?"
    old = "(\(?\s*starych\s*\)?)?"
    numbers_as_words = "(\(.*\))?"
    pln = "(zł)"
    combined = f"{number}{decimal_part}\s*{magnitudes}\s*{old}{numbers_as_words}\s*{pln}"
    return re.compile(combined)


root_dir = '/home/marcin/Desktop/SemestrVIII/PJN/lab1'
tmp_path = f"{root_dir}/tmp/output.txt"
output_file = open(tmp_path, 'r')
pattern = prepare_regex()
results = []

for line in output_file:
    res = pattern.search(line)
    if res is not None:
        match = res.groups()
        numeric_match = res.group('number')
        magnitude_match = res.group('magnitude')
        decimal_match = res.group('decimal')
        float_nr = normalize_match(numeric_match, decimal_match, magnitude_match)
        results.append((match, line, float_nr))

print(results)
