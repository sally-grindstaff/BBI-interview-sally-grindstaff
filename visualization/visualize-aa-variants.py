#!/usr/bin/env python

#%%
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import json

#%%
with open('test.json', 'r') as fh:
    json_array = json.load(fh)
df = pd.DataFrame(json_array) 
with open('test_aa_seq.txt', 'r') as fh:
    wt_seq = fh.read()

#%% 
# add wildtype entries to df
for i,aa in enumerate(wt_seq):
    df.append({
        'position': i,
        'substitution': aa,
        'score': 1
    },
    ignore_index=True
    )

#%%
# pivot wide
df_wide = df.pivot(index='substitution', columns='position', values='score')

#%%
# customize colormap norm so that -0.5 is just as dark as +2.5
divnorm = mcolors.TwoSlopeNorm(vcenter=0, vmin=-0.5, vmax=2.5)
#%%
heat_map = sb.heatmap(df_wide, cmap="RdBu_r", norm=divnorm)
plt.show()


# %%
