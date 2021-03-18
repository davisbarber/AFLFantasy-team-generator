import numpy as np
import pandas as pd

def contains_duplicates(X):
    return len(np.unique(X)) != len(X)

def get_total_salary(players, data):
    return data.loc[list(players), 'price'].sum()