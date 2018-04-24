import json
import pandas
import os
import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from  itertools import tee, chain, islice, groupby
from math import log
from operator import itemgetter,attrgetter
from itertools import takewhile
import requests
import re
from collections import namedtuple 
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier 
from sklearn.metrics import classification_report
from constants import *
Category = namedtuple('Category',['label','caseNumber'])
Text = namedtuple('Text',['id','words'])
WithCategory = namedtuple('WithCategory', ['judgement','category'])
Line = namedtuple('Line', ['id','words','category'])

def extract_file_number(filename):
    return int(filename.split('-')[1].split('.')[0])

def is_2017_in_file(filename):
    return 2716 <= extract_file_number(filename) <= 3163

def is_2018_in_file(filename):
    return 3163 <= extract_file_number(filename) <=  3173

def clean_text(line,common_words):
    justification = line.split('<h2>UZASADNIENIE</h2>')[1]
    notags = re.sub(r"<[^>]*>", " ", justification)
    nobreaks = re.sub(r"-\n", " ", notags)
    nodigits = re.sub(r"\d+", " ", nobreaks)
    noromans = re.sub(r"\b[XVILMC]+\b", "", nodigits)
    lower = noromans.lower()
    words = filter(lambda x: x not in common_words, re.findall(r"\w+", lower))
    return ' '.join(words)

def filter_judgements(judgement):
    return year in judgement['judgmentDate']  and \
    judgement['courtType'] in ['COMMON', 'SUPREME'] and \
    '<h2>UZASADNIENIE</h2>' in judgement['textContent']


def map_category(judgement):
    caseNumber = judgement['courtCases'][0]['caseNumber'].split(' ')
    _, label = next(
        filter(lambda pat: pat[0].match(caseNumber[1]), patterns.items()))
    return Category(label, caseNumber)


def judgements_raw(filename, json_data_dir):
    with open(os.path.join(json_data_dir, filename), 'r') as jsonFile:
        judgements = json.load(jsonFile)['items']
    return judgements

def clean_tagged(line):
    _id, text = line
    words = filter(lambda word: word not in common_tagged_words,
                   text.split(' '))
    return Text(_id,' '.join(words).split('uzasadnienie',1)[1]) 

def tagged(categories_by_id):
    lines = map(lambda l: Text._make(l.split('; ')),
                open(tagging_file, 'r'))
    int_id = map(lambda l: (int(l[0]),l[1]),lines)
    filtered = filter(lambda l: l[0] in categories_by_id, int_id)
    cleaned = map(clean_tagged, filtered)
    return map(
        lambda text: Line(text.id, text.words, categories_by_id[text.id]),
        cleaned)

mapping = {
    'civil': [1,0,0,0],
    'criminal': [0,1,0,0],
    'economic': [0,0,1,0],
    'insurance': [0,0,0,1],
          }

def get_train_test_data(listed_data): 
    data_x, data_y = zip(*listed_data)
    data_y = list(map(lambda x: mapping[x],data_y))
    data_x = np.expand_dims( np.array(data_x), axis=1)
    data_y = np.array(data_y) 
    stratified_split = StratifiedShuffleSplit(n_splits=2, test_size=0.25)

    for train_index, test_index in stratified_split.split(data_x,data_y):
        x_train, x_test = data_x[train_index], data_x[test_index]
        y_train, y_test = data_y[train_index], data_y[test_index]
    x_train = [x[0].strip() for x in x_train.tolist()]
    x_test = [x[0].strip() for x in x_test.tolist()]

    return x_train, x_test, y_train,y_test
