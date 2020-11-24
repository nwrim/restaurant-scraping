'''
Scraping allmenus.com

Nak Won Rim, Anqi Hu, Chia-yun Chang
'''

import requests
import json
import pickle
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from urllib.parse import urlparse
from sklearn.preprocessing import MultiLabelBinarizer
from mapping_dict import clean_cuisine_name


with open('mapping_dict.pkl', 'rb') as pkl:
    MAPPING_DICT = pickle.load(pkl)


class Scraper():
    '''
    class storing scraper
    '''
    
    def __init__(self):
        '''
        Constructor for the Scraper class
        '''

        self.core_url = 'https://www.allmenus.com/il/chicago/-/'
        self.cuisine_set = set()
        self.url_set = set()


    def __repr__(self):
        '''
        Representation for the Scraper class: displays the list of cuisines to
        scrape
        '''
        
        return ('Scraper for scraping Chicago restaurant information from' +
                'allmenus.com.\nthe Scraper will scrape the restaurant with' +
                'following cuisines: \n' + str(self.cuisine_set))


    def add_all_cuisines(self):
        '''
        Go to the core url, collect all cuisines listed in the page and
        add it to the set of cuisines to scrape
        '''

        rqst = requests.get(self.core_url)
        soup = BeautifulSoup(rqst.text, 'html.parser')
        cusine_container = soup.find('div', class_='cuisine-container')
        for c in cusine_container.find_all('div', class_='s-checkbox-group'):
            self.cuisine_set.add(clean_cuisine_name(c.text))


    def add_cuisine(self, cuisine):
        '''
        Manually add a cuisine name to scrape

        Input:
          cuisine (str): the cuisine to scrape
        '''

        self.cuisine_set.add(clean_cuisine_name(cuisine))


    def get_url_set(self):
        '''
        From each cuisine in the cuisine set, retrieve all the restaurant urls
        belonging to that cuisine and add it to set of url to scrape.
        '''

        for cuisine in self.cuisine_set:
            sleep(4)
            rqst = requests.get(self.core_url + cuisine)
            if rqst.status_code != 200:
                print(cuisine, 'is not a valid cuisine')
                continue
            soup = BeautifulSoup(rqst.text, 'html.parser')
            restaurants = soup.find_all('li', class_='restaurant-list-item')
            if not restaurants:
                print(cuisine, 'is not a valid cuisine')
                continue
            for r in restaurants:
                if 'Chicago' not in r.find_all('p', class_='address')[1].text:
                    continue
                url = r.find('a', class_=None).get('href')
                if not urlparse(url).netloc:
                    url = "https://www.allmenus.com" + url
                if urlparse(url).netloc != "www.allmenus.com":
                    continue
                self.url_set.add(url) 


    def scrape_menus(self):
        '''
        Scrape all the urls in the set of urls. Write a pickle file to store
        the final dataframe.

        Return:
          df (pandas dataframe): the pandas dataframe 
        '''

        menus_dict = {}
        for idx, url in enumerate(self.url_set):
            sleep(4)
            scraped = scrape_menu(idx, url)
            if scraped:
                menus_dict.update(scraped)
        df = pd.DataFrame(menus_dict).T
        mlb = MultiLabelBinarizer()
        df = pd.concat([df, pd.DataFrame(mlb.fit_transform(df['Cuisine']),
                                         columns=mlb.classes_, 
                                         index=df.index)], axis=1)
        return df

            
def scrape_menu(idx, url):
    '''
    Scrape a menu from single restaurant url. Retrieve the json file in the
    website and index through/process the data. Returns a dictionary that
    stores the information that is eventually converted into a dataframe in
    Scraper.scrape_menus().

    Input:
      idx (int): the index for the dictionary (that will become the index of
                 the dataframe in Scraper.scrape_menus)
      url (str): the restaurant url to scrape

    Return:
      (dict) a dictionary that will become a row in the final data frame
             (created by Scraper.scrape_menus)
    '''

    rqst = requests.get(url)
    soup = BeautifulSoup(rqst.text, "html.parser")
    tmp = soup.find("script", type="application/ld+json")
    try:
        restaurant_json = json.loads(tmp.text, strict=False)
    except:
        return None
    section_prices = []
    try:
        menu_sections = restaurant_json["hasMenu"][0]["hasMenuSection"]
        for section in menu_sections:
            section_price = get_section_price(section)
            if section_price:
                section_prices.append(section_price)
    except:
        pass
    if not section_prices:
        return {}
    return {idx: {"Cuisine": map_cuisines(restaurant_json["servesCuisine"]),
                  "Restaurant": restaurant_json["name"],
                  "Coordinate": (restaurant_json["geo"]["longitude"], 
                                   restaurant_json["geo"]["latitude"]),
                  "Address": restaurant_json["address"]["streetAddress"],
                  "Price": np.median(section_prices)}}


def get_section_price(section):
    '''
    Get the mean price of a restaurant section ex) drinks, entree, main dish

    Input:
      section (dict): dictionary contaning the section information of a
                      restaurant menu
    Return:
      (float) the mean price of this restaurnat menu section
    '''

    all_price = []
    for item in section.get("hasMenuItem", []):
        try:
            all_price.append(float(item["offers"][-1]["Price"]))
        except:
            pass
    if all_price:
        return np.mean(all_price)
    return None


def map_cuisines(cuisines):
    '''
    Map the cuisines according to pre-constructed mapping dictionary ex)
    pasta -> italian, italian -> italian

    Input:
      cusines (list): list of cuisines to be mapped
    Returns
      result (list): list of mapped cuisines
    '''

    result = []
    for cuisine in cuisines:
        cuisine = clean_cuisine_name(cuisine)
        if cuisine in MAPPING_DICT.keys():
            result.append(MAPPING_DICT[cuisine])
    return result
