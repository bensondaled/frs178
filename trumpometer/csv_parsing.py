from collections import deque
from io import StringIO
import pandas as pd

def read_last_nrows(fname, n, lock=None):
    columns = pd.read_csv(fname, nrows=0).columns

    with open(fname, 'r') as f, lock:
        q = deque(f, n)
    try:
        result = pd.read_csv(StringIO(''.join(q)), header=None)
        result.columns = columns
        return result
    except:
        return None

def dump_data(data, destination='data/data.csv'):
    """
    data should be a pd.Series with index of state abbreviations and values of sentiments
    """
    template = pd.read_csv('data/states_raw.csv')
    template.index = template.abbreviation
    template.loc[:,'sentiment'] = 0
    for state,val in data.iteritems():
        template.loc[state,'sentiment'] += val
    template.to_csv(destination)
