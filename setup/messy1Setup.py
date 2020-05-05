# create a list of each unique api call in order

import os
from joblib import load, dump
import re
import csv


# create a list of each unique api call in order
# create a list of each unique api call for each of the classes
'''
    with open('all_analysis_data.txt', 'r') as original_data:
    api_calls = original_data.readlines()

labels = []
with open('labels.csv', 'r') as data_labels:
    for line in data_labels.readlines():
        labels.append(line.replace('\n', ''))

set_of_all_call = set()
for call_seq in api_calls:
    for call in call_seq.split(' '):
        call = re.sub('\n', '', call)
        set_of_all_call.add(call)

set_of_all_call = list(set_of_all_call)

sets = {}
set_labels = list(set(labels))
for label in set_labels:
    sets[label] = set()

i = 0
for call_seq in api_calls:
    for call in call_seq.split(' '):
        call = re.sub('\n', '', call)
        sets[labels[i]].add(call)
    i += 1

dump(set_of_all_call, 'all_api_call_order.joblib')
for key in sets.keys():
    dump(sets[key], f'{key}_api_call_order.joblib')
    
    labels = []
with open('labels.csv', 'r') as data_labels:
    for line in data_labels.readlines():
        labels.append(line.replace('\n', ''))

sets = {}
set_labels = list(set(labels))
for label in set_labels:
    sets[label] = set()

i = 0
for call_seq in api_calls:
    for call in re.sub('\n', '', call_seq).split(' '):
        sets[labels[i]].add(call)
    i += 1

# create a file of (0, N) with api calls in order

total = load('all_api_call_order.joblib')
with open('total_co.csv', 'w') as out_file:
    for item in total:
        out_file.write(str(item) + ',')

for key in sets.keys():
    data = load(f'{key}_api_call_order.joblib')
    with open(f'{key}_co.csv', 'w') as out_file:
        for item in data:
            out_file.write(str(item) + ',')
    
'''

import re
import pandas as pd

if __name__ == '__main__':
    with open('all_analysis_data.txt', 'r') as original_data:
        api_calls = original_data.readlines()

    with open('labels.csv', 'r') as in_file:
        labels = in_file.readlines()

    index_df = pd.read_csv('index.csv')
    index_df.columns = ['index']

    rows = index_df.values

    temp_calls = []
    temp_labels = []

    for i in range(len(api_calls)):
        if i in rows:
            temp_calls.append(api_calls[i].split(' '))
            temp_labels.append(re.sub(r'\n', '', labels[i]))
    del api_calls

    sequence = []
    for call_list in temp_calls:
        for call in call_list:
            if call not in sequence:
                sequence.append(call)

    final_call = []
    for call_list in temp_calls:
        call_list_temp = []
        for call in call_list:
            for i in range(len(sequence)):
                call_list_temp.append(i)
        final_call.append(call_list_temp)
    del temp_calls

    return_list = []
    for call_list in final_call:
        return_list.append(" ".join(call_list))

    index_df['label'] = temp_labels
    index_df['api'] = return_list

    print(index_df.head())

    grab_df = index_df.sample(400).sort_index()

    grab_df.to_csv('working_sample.csv')
