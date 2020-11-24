'''
Getting census tract of restaurant and retrieving income data of that tract

Nak Won Rim, Anqi Hu, Chia-yun Chang
'''

import re
import pandas as pd
import numpy as np
import censusgeocode as cg

INCOME = pd.read_csv('data/Income_by_Location.csv')
INCOME = INCOME[INCOME['Year'] == 2017][['Household Income by Race',
                                         'Geography']]
INCOME['Tract'] = [re.sub(', .*', '', i.strip('Census Tract')) for i in 
                   INCOME['Geography']]
INCOME.drop(columns=['Geography'], inplace=True)
INCOME.columns = ['Income', 'Tract']


def get_tract(address):
    '''
    Obtains census tract information and returns the tract number if the 
    address matches the census database. Otherwise, returns NaN.

    Inputs:
        address(str): the street address of a restaurant

    Outputs:
        tract_num(str): the tract number of the address or NaN.
    '''

    info = cg.address(address.upper(), city='Chicago', state='IL')
    if info:
        tract = info[0]['geographies']['2010 Census Blocks'][0]['TRACT']
        t = tract[:4] + '.' + tract[-2:]
        t = t.strip('0')
        tract_num = t.strip('.')
    else: 
        tract_num = np.nan
    return tract_num


def get_income(tract):
    '''
    Matches income from the median household income dataset

    Inputs:
        tract(str): the census tract number 

    Outputs:
        The annual median household income for the census tract. If no 
        matching income was found, return NaN.
    '''

    income = INCOME[INCOME['Tract'] == tract]['Income']
    if not income.empty:
        return income.iloc[0]
    return np.nan

 