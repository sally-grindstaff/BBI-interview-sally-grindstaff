# Heatmap visualization
This program creates a heatmap to visualize the effects of amino acid substitutions on protein function.

## Requirements
- Python 3
- pandas
- matplotlib
- seaborn

See [here](visualization_env.yml) for the conda environment I used.

## How to use
There are 2 options: run visualize-aa-variants.py from the command line to generate a PNG with the heatmap, or run visualize-aa-variants.ipynb interactively with Jupyter Notebook.

## Run from command line
Input:  
- JSON file containing array
  - Required array structure:  
    [
     {
      'position': \<int\>,
      'substitution': \<str\>,
      'score': \<flt\>
     },
     {
      'position': \<int\>,
      'substitution': \<str\>,
      'score': \<flt\>
     }
    ]
  - Object names must be 'position', 'substitution', and 'score', spelled correctly and lowercase. This is something I would want to fix if I were to continue working on this program.
- Text file containing wildtype amino acid sequence as a one-line string with no spaces. Must be no more than 40 characters in length.  

Output:
- Path/filename to PNG file to output.
  
Usage:  
./visualize-aa-variants.py [-h] -s SEQUENCE -a ARRAY -o OUTPUT

## Run interactively
To run interactively, open visualize-aa-variants.ipynb as a Jupyter Notebook and enter array (using structure described in above section) and wildtype sequence manually, or enter filepaths. This option does not save the heatmap as a PNG, but displays it interactively in the notebook.
