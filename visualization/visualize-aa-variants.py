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

def add_wt_to_df(wildtype_seq, dataframe):
    '''Takes a wildtype sequence and existing dataframe, and adds one entry per amino acid to the dataframe, with the variant score equal to 1.'''
    position_list = []
    substitution_list = []
    score_list = []
    for i, aa in enumerate(wildtype_seq):
        position_list.append(i+1) # we are using 1-based indexing for position in sequence
        substitution_list.append(aa)
        score_list.append(1)
    wildtype_df = pd.DataFrame(
        {'position': position_list,
        'substitution': substitution_list,
        'score': score_list}
        )
    new_df = pd.concat([dataframe, wildtype_df]) # combine existing dataframe with new wildtype dataframe
    return new_df

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

# check that wildtype sequence does not exceed 40 amino acids
seq_len = len(wt_seq)
if seq_len > 40:
    raise SystemExit('Error: Length of wildtype sequence exceeds limit (40 amino acids).')

# add wildtype entries to df to differentiate them from truly missing values
df = add_wt_to_df(wt_seq, df)

# pivot wide
df_wide = df.pivot(index='substitution', columns='position', values='score')
# mask missing entries
mask = df_wide.isnull()
# generate heatmap
heat_map = sb.heatmap(df_wide, cmap="RdBu_r", center=1, mask=mask)
heat_map.set_facecolor('black') # missing entries show up as black
plt.show()
plt.savefig(fig_path)
