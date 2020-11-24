'''
Execute a sample data collection and processing (1 Cuisine, 2 Restaruants)

Team FRA (Front Row Asians): Anqi Hu, Chia-yun Chang, Nak Won Rim
'''

import scraper
import tract_income
import inspection
import count_crime
import pandas as pd

def test():
    '''
    A test code for go() function in go.py. Scrapes only one cuisine from
    allmenus.com (resulting in two restaurants), add the census tract of
    restaurants, area median income of restaurants, most recent food
    inspection result of restaurant and the number of crimes that happened
    within 0.8 kms of restaurant.
    Creates 'sample.pkl', which is a pickle file that containing the created
    sample data.
    '''

    sc = scraper.Scraper()
    sc.add_cuisine('Afghan')
    sc.get_url_set()
    df = sc.scrape_menus()
    df['Tract'] = df['Address'].apply(tract_income.get_tract)
    df['Income'] = df['Tract'].apply(tract_income.get_income)
    df['Inspection'] = df.apply(inspection.get_inspection, axis=1)
    df2 = pd.DataFrame(df['Coordinate'].apply(count_crime.count_crimes))
    df = pd.merge(df, df2, left_index=True, right_index=True)
    df.columns = [c.title() for c in df.columns]
    df.drop(columns=['Address', 'Cuisine'], inplace=True)
    df.to_pickle('sample.pkl')

if __name__ == "__main__":
    test()
