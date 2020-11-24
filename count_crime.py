'''
Count the number of crimes of recent year that happened in the parameter of
each restaurant

Team FRA (Front Row Asians): Anqi Hu, Chia-yun Chang, Nak Won Rim
'''

import pandas as pd
import numpy as np
from math import sin, cos, sqrt, atan2, radians

CRIMES = pd.read_csv('data/crimes_type.csv')
CRIMES.columns = ['Longitude','Latitude','Type']
CRIMES = CRIMES[CRIMES['Type'] != 'NON-CRIMINAL']
LAT_MARG = 0.008994
LON_MARG = 0.011915
R = 6378.1370

def find_filter(coordinate):
    '''
    Find the coordinate of the circumscribed sqaure of the parameter.
    Filtering the coordinates first using makes in_radius much faster.
    
    Input:
      coordinate (tuple): tuple contaning the coordinate for a restaurant
    '''

    return [float(coordinate[0]) + LON_MARG, 
            float(coordinate[0]) - LON_MARG,
            float(coordinate[1]) + LAT_MARG,
            float(coordinate[1]) - LAT_MARG]


def in_radius(loc1, loc2):
    '''
    Calcuate distance in kilometer between two locations(lists or tuples). 
    Return True if distance is under 0.8km, False if not.

    Input:
      loc1, loc2 (tuple): (longitude, latitude) of a location coordinate

    Returns:
      (Bool) True if distance is under 0.8km, False if not
    '''

    lat1 = radians(float(loc1[0]))
    lon1 = radians(float(loc1[1]))
    lat2 = radians(loc2[0])
    lon2 = radians(loc2[1])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c    
    return distance < 0.8


def count_crimes(coordinate):
    '''
    Count the number of crimes that happened within 0.8km of given coordinate
    
    Input:
      coordinate (tuple): (longitude, latitude) of a location coordinate

    Returns:
      counts (pandas Series): a Series containing the number of crimes that
                              happened within 0.8 km of given coordinate,
                              indexed by the type of the crime
    '''

    filt = find_filter(coordinate)
    coordinate = (float(coordinate[0]), float(coordinate[1]))
    crimes = CRIMES[(CRIMES['Longitude'] <= filt[0]) & 
                    (CRIMES['Longitude'] >= filt[1]) &
                    (CRIMES['Latitude'] <= filt[2]) & 
                    (CRIMES['Latitude'] >= filt[3])]
    tmp = crimes.apply(lambda x: in_radius(coordinate,
                                           (x['Longitude'], x['Latitude'])),
                                           axis=1)
    crimes = crimes[tmp]
    counts = crimes['Type'].value_counts()
    counts = counts.append(pd.Series({'SUM': sum(counts)}))
    return counts
