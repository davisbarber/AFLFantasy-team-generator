import pandas as pd
from constants import *
import string

# various helper functions to format player data


def format_player_data(data):
    """Formats raw player data from google sheet and returns usable dataframe

    Args:
        data ([dataframe]): [player data]

    Returns:
        [dataframe]: [formatted player data]
    """
    # fill pos2 blank rows
    data.loc[:,POSITION2] = data.loc[:,POSITION2].fillna('')
    # only use players with include = 1
    data = data.loc[data.include == 1, :]
    # convert price to int
    df = data.copy()
    df.loc[:,PRICE] = data.loc[:,PRICE].str.strip('$k').astype('int')
    
    # add price category column
    df = add_price_category(df)
    
    # add column for average between all score columns
    df.loc[:, COMBINED] = df.loc[:, (AVERAGE, PROJECTED, LAST3AVG, AAMI)].mean(axis = 1)
    return df


def add_price_category(data):
    price_category = []

    for value in data[PRICE]:
        if value > 650:
            price_category.append(PREMIUM)
        elif value > 270:
            price_category.append(MID_PRICE)
        else:
            price_category.append(ROOKIE)

    df = data.copy()
    df.loc[:,PRICE_CAT] = price_category
    return df

def format_price_str(x):
    return x.strip('$k')