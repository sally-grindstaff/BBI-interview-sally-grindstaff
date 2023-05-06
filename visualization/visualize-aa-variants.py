#!/usr/bin/env python

import argparse
from pathlib import Path
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import json

def get_args():
    parser = argparse.ArgumentParser(description='Generates a heatmap visualization from a wildtype amino acid sequence and a corresponding array defining amino acid substitutions and their protein variant scores.')
    parser.add_argument('-s', '--sequence', help='Path to text file containing one-line amino acid sequence for wildtype protein. This program currently only accepts sequences of length <=40.', required=True, type=str)
    parser.add_argument('-a', '--array', help='Path to JSON array file containing one entry per variant, where each entry contains three objects: "position", "substitution", and "score". Entries must follow this naming scheme, and object names must be lowercase as shown.', required=True, type=str)
    parser.add_argument('-o', '--output', help='Path to output PNG file.', required=True, type=str)
    return parser.parse_args()

args = get_args()

# create Path objects
array_path = Path(args.array)
seq_path = Path(args.sequence)
fig_path = Path(args.output)

# load array from JSON
with open(array_path, 'r') as fh:
    json_array = json.load(fh)
# convert array to DataFrame
df = pd.DataFrame(json_array)

# load wildtype sequence
with open(seq_path, 'r') as fh:
    wt_seq = fh.read()

# add wildtype entries to df to differentiate them from truly missing values
for i,aa in enumerate(wt_seq):
    df = df.append({
        'position': i+1, # we are using 1-based indexing for position in sequence
        'substitution': aa,
        'score': 1 # score of wildtype amino acid is 1 by default
    },
    ignore_index=True
    )

# pivot wide
df_wide = df.pivot(index='substitution', columns='position', values='score')
# mask missing entries
mask = df_wide.isnull()
# generate heatmap
heat_map = sb.heatmap(df_wide, cmap="RdBu_r", center=1, mask=mask)
heat_map.set_facecolor('black') # missing entries show up as black
plt.show()
plt.savefig(fig_path)
