import pandas as pd

# ==================================================
# PRE-PROCESS SRT FILES
# ==================================================

def srt_to_df(srt_file):
    """
    Reads srt file
    Removes line numbers and times
    Returns dataframe
    """
    df = pd.read_csv(srt_file, sep='\n', header=None, names=['lines'])

    ls_times = df[df.lines.str.contains('-->')].index.tolist()
    ls_nums = [i - 1 for i in ls_times]

    df = df[~df.index.isin(ls_nums)]

    clean_lines = []
    for line in df.lines:
        if '-->' in line:
            clean_lines.append('')
        else:
            merged_line = clean_lines[-1] + ' ' + line
            clean_lines[-1] = merged_line.strip()

    return clean_lines