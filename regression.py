'''
Run the OLS regression on the final data set

Team FRA (Front Row Asians): Anqi Hu, Chia-yun Chang, Nak Won Rim
'''

import pandas as pd
import numpy as np
import statsmodels.api as sm

def regression():
    '''
    Takes in the cleaned dataset and prints an OLS regression summary, using
    all available variables for cuisine categories, crime types and inspection
    results
    '''

    raw = pd.read_pickle('final.pkl')
    temp = raw[((raw['Inspection'].isin(['Fail', 'Pass', 'Pass w/ Conditions', 
                                         'Out of Business'])) & 
                (raw['Price'] < 40))]
    dums = pd.get_dummies(temp['Inspection'])
    final = pd.concat([temp, dums], axis=1)
    final.drop(columns=['Inspection', 'Coordinate', 'Restaurant'],
               inplace=True)
    final.dropna(subset=['Income'], inplace=True)
    final.drop(columns=['Tract'], inplace=True)
    final = final.astype({'Price': 'float64'})
    final = final.fillna(0)
    x = final.drop(columns=['Price'])
    y = final['Price']
    x = sm.add_constant(x)
    lm = sm.OLS(y, x)
    res = lm.fit()
    print(res.summary())

if __name__ == "__main__":
    regression()
