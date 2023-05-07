#!/usr/bin/env python

import json
import random

wildtype_seq = 'MARND'
aa_set = set('ARNDCEQGHILKMFPSTWYV')

my_array = []
for i in range(len(wildtype_seq)):
    for aa in aa_set:
        if aa == wildtype_seq[i]:
            continue
        my_array.append({
            'position': i+1,
            'substitution': aa,
            'score': random.uniform(-0.5,2.5)})

# example_array = [
#     {'position': 1,
#     'substitution': 'A',
#     'score': 1.2},
#     {'position': 1,
#     'substitution': 'E',
#     'score': 0.6}
# ]

with open('test.json', 'w') as fh:
    json.dump(my_array, fh, indent=4)
