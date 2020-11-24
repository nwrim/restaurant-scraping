'''
Execute entire data collection and processing

Nak Won Rim, Anqi Hu, Chia-yun Chang
'''

import scraper
import tract_income
import inspection
import count_crime
import pandas as pd

def go():
    '''
    The final scraping and data processing function. Scrapes all cuisines from
    all available restaurants in Chicago from allmenus.com, add the census
    tract of restaurants, area median income of restaurants, most recent food
    inspection result of restaurant and the number of crimes that happened
    within 0.8 kms of restaurant.
    Creates 'final.pkl', which is a final pickle file that contains all data.
    Also creates 'data/scrape_final.pkl', which is the pickle file containing
    only the results from scraping. Note that this was a safe measure and it
    is not included in the final repository.
    '''

    sc = scraper.Scraper()
    sc.add_all_cuisines()
    sc.get_url_set()
    df = sc.scrape_menus()
    df.to_pickle('data/scrape_final.pkl')
    df['Tract'] = df['Address'].apply(tract_income.get_tract)
    df['Income'] = df['Tract'].apply(tract_income.get_income)
    df['Inspection'] = df.apply(inspection.get_inspection, axis=1)
    df2 = pd.DataFrame(df['Coordinate'].apply(count_crime.count_crimes))
    df = pd.merge(df, df2, left_index=True, right_index=True)
    df.columns = [c.title() for c in df.columns]
    df.drop(columns=['Address', 'Cuisine'], inplace=True)
    df.to_pickle('final.pkl')

if __name__ == "__main__":
    go()