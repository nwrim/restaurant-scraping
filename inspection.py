'''
Getting The most recent inspection data of restaurants

Nak Won Rim, Anqi Hu, Chia-yun Chang
'''

import jellyfish
import pandas as pd

INSPECTION = pd.read_csv('data/Inspection.csv')

def jw(string1, string2):
    '''
    Calculate jw distance between two strings

    Inputs:
        string1(str): a string of characters
        string2(str): a string of characters

    Outputs:
        The Jaro-Winkler distance between the two strings.
    '''

    return jellyfish.jaro_winkler(string1, string2)


def get_inspection(row):
    '''
    Obtains the latest food safety inspection result for a restaurant

    Inputs:
        row: a row of restaurant-related information 

    Outputs:
        Matched inspection results if the restaurant information was found.
        Otherwise, return None.

    '''
    first4 = row['Address'][:4]
    high_jw = 0.667
    match = ''
    for entry in INSPECTION.itertuples(index=False):
        if entry[2][:4] == first4:
            new_jw = jw(row['Restaurant'].lower(), entry[0].lower())
            if new_jw > high_jw:
                high_jw = new_jw
                match = entry
    if not match:
        return None
    return match[4]