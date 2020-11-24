'''
Creating Mapping Dictionary for Cuisine Classification

Team FRA (Front Row Asians): Anqi Hu, Chia-yun Chang, Nak Won Rim
'''

import requests
import re
import pickle
from bs4 import BeautifulSoup
from time import sleep
from collections import Counter 


CORE_URL = 'https://www.allmenus.com/il/chicago/-/'

def get_all_cusines(CORE_URL):
    '''
    Extract all cuisine categories for all restaurant in Chicago registered
    in allmenu.com.

    Input: CORE_URL (str): the url for the allmenu.com Chicago directory

    Returns: cusine_set (set): a set containing all cusine categories for all
                              restaruant in Chicago registered in allmenus.com
    '''

    rqst = requests.get(CORE_URL)
    soup = BeautifulSoup(rqst.text, 'html.parser')
    cusine_container = soup.find('div', class_='cuisine-container')
    cuisine_set = set()
    for div in cusine_container.find_all('div', class_='s-checkbox-group'):
        cuisine_set.add(clean_cuisine_name(div.text))
    return cuisine_set


def clean_cuisine_name(cuisine):
    '''
    Clean the cuisine name to standardize

    Input:
      cuisine (str): the cuisine name to be standardized

    Returns:
      cuisine (str): the standardized cuisine name
    '''

    cuisine = re.sub("[/\s\)]", "", cuisine.strip().lower())
    cuisine = re.sub('&amp;|[\(&]', "-", cuisine)
    if cuisine == "delifood":
        cuisine = "deli"
    elif cuisine == "eclectic-international":
        cuisine = "eclectic"
    elif cuisine == "noodles":
        cuisine = "noodle-bar"
    elif cuisine == "potatoes":
        cuisine = "potato"
    elif cuisine == "subs":
        cuisine = "sub"
    return cuisine


def get_num_rest_and_combi(cuisine_set, CORE_URL):
    '''
    Extract the number of restaurant for all the cuisine categories in the
    cuisine_set and store it in a dictionary

    Input:
      cusine_set (set): a set containing all cusine categories for all
                        restaruant in Chicago registered in allmenus.com
      CORE_URL (str): the url for the allmenu.com Chicago directory

    Returns: 
      num_rest (dict): dictionary containing the number of restaurant for
                       cuisine categories
      cui_combi (list of list): a list of lists of unique cusine combinations
                                ex) [[american, chicagogrill], [italian]]
    '''

    num_rest = {}
    cui_combi = []
    for cuisine in cuisine_set:
        sleep(4)
        rqst = requests.get(CORE_URL + cuisine)
        if rqst.status_code != 200:
            print(cuisine, "is not a valid cuisine")
            continue
        soup = BeautifulSoup(rqst.text, "html.parser")
        num = len(soup.find_all("li", class_="restaurant-list-item"))
        for cuisine_com in soup.find_all('p', class_='cousine-list'):
            if cuisine_com not in cui_combi:
                combi = cuisine_com.text.split(', ')
                if combi not in cui_combi:
                    cui_combi.append(combi)
        if num == 0:
            continue
        num_rest[cuisine] = num
    return num_rest, cui_combi


def get_top_40(num_rest):
    '''
    Get the top 40 elements that has highest value in the num_rest. This
    method was picked up from: 
    https://www.geeksforgeeks.org/python-program-to-find-the-highest-3-values-in-a-dictionary/

    Input:
      num_rest (dict): dictionary containing the number of restaurant for
                       cuisine categories
    Returns:
      (set) set of top 40 elements most frequent in the dataset
    '''

    return {c[0] for c in Counter(num_rest).most_common(40)}


def get_combi_to_map(cui_combi, top_40):
    '''
    get cuisine combination that does not contain at least one top 40 cuisines

    Input:
      cui_combi (list of list): a list of lists of unique cusine combinations
                                ex) [[american, chicagogrill], [italian]]
      top_40 (set): set of top 40 cuisines ex) {italian, american}
    '''
    
    combi_to_map = []
    for combi in cui_combi:
        in_top_40 = False
        for cuisine in combi:
            cuisine = clean_cuisine_name(cuisine)
            if cuisine in top_40:
                in_top_40 = True
                break
        if not in_top_40:
            combi_to_map.append(combi)
    return combi_to_map


def exploration(test):
    '''
    Explore the cuisines and associated restaruant in Chicago. Find out the
    top 40 restaurants that could independently be a category. Also find out
    all cuisine combination that does not include any of the top 40 cusines
    so we can create a mapping dictionary that groups some cuisines together
    in a way that all restaurants are classified with at least one cuisine. 

    Input:
      test (bool): if True, we will use the stored data instead of scraping
                   data
    Output:
      if test was False, we will scrape the data and store the set of top 40
      cuisines and list of lists of unique cuisine combination as pickle.
    '''

    if not test:
        with open('data/num_rest_for_cui.pkl', 'rb') as pkl:
            num_rest = pickle.load(pkl)
        top_40 = get_top_40(num_rest)
        with open('data/cui_combi.pkl', 'rb') as pkl:
            cui_combi = pickle.load(pkl)
        combi_to_map = get_combi_to_map(cui_combi, top_40)
    else:
        cuisine_set = get_all_cusines(CORE_URL)
        num_rest, cui_combi = get_num_rest_and_combi(cuisine_set, CORE_URL)
        top_40 = get_top_40(num_rest)
        combi_to_map = get_combi_to_map(cui_combi, top_40)
        with open('data/num_rest_for_cui.pkl', 'wb') as pkl:
            pickle.dump(num_rest, pkl)
        with open('data/cui_combi.pkl', 'wb') as pkl:
            pickle.dump(cui_combi, pkl)
    print('The top 40 cuisines are: \n', top_40, 
          '\nThe cuisine combination that needs mapping are: \n', 
          combi_to_map)


def validation():
    '''
    Make sure that all cuisine combination has at least one component that is
    mapped in the mapping_dict
    '''

    with open('data/cui_combi.pkl', 'rb') as pkl:
        cui_combi = pickle.load(pkl)
    with open('mapping_dict.pkl', 'rb') as pkl:
        mapping_dict = pickle.load(pkl)    
    # restaurants with following combination were all invalid (didn't have 
    # proper menu)
    cui_combi.remove(['Pub Food'])
    cui_combi.remove(['Crepes'])
    cui_combi.remove(['Subs'])
    covered = mapping_dict.keys()
    not_covered = []
    for combi in cui_combi:
        combi_covered = False
        for cuisine in combi:
            if clean_cuisine_name(cuisine) in covered:
                combi_covered = True
                break
        if not combi_covered:
            not_covered.append(combi)
    if not not_covered:
        print('All cuisine categories were classified!')
    else:
        print('Following cuisine was not classified:', not_covered)


if __name__ == "__main__":
    msg = 'enter 0 for finding the top 40 cuisines by the number of ' + \
          'restaurants and all cuisine combination not having one of the ' + \
          'top 40 cuisines\nenter 1 for validating that all restaurants' + \
          'got at least one classification: '
    validate = input(msg)
    while validate not in ['0', '1']:
        validate = input('valid input are 0 or 1. Try Again: ')
    validate = int(validate)
    if validate:
        validation()
    else:
        test = input('enter 0 if you want to use scraped data \n' + \
                     'enter 1 if you want to scrap the website again: ')
        while test not in ['0', '1']:
            test = input('valid input are 0 or 1. Try Again: ')
        test = int(test)
        exploration(bool(test))
