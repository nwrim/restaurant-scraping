'''
Visulalize the data

Nak Won Rim, Anqi Hu, Chia-yun Chang
'''

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import descartes
from shapely.geometry import Point
import numpy as np

SAVE_PATH = 'graph/'

## This part is done plot by plot. We did not write a generalizable function 
## for the plots due to the fact that each visualization has its distinct 
## setting.

################
#Plot Map plots#
################

chicago = gpd.read_file('data/chicago_shape/chicago.shp')
allmenus = pd.read_pickle('final.pkl')
allmenus['Longitude'] = [float(x[0]) for x in allmenus['Coordinate']]
allmenus['Latitude'] = [float(x[1]) for x in allmenus['Coordinate']]
allmenus['Price'] = allmenus['Price'].astype(float)
geo_df = gpd.GeoDataFrame(allmenus, 
   geometry=gpd.points_from_xy(allmenus['Longitude'], allmenus['Latitude']))

# restaurant prices 
fig, ax = plt.subplots(figsize=(12,12))
chicago.plot(ax=ax, color='gray')
geo_df[(geo_df['geometry'].apply(lambda x: x.coords[:][0][0] > -88)) 
                              & (geo_df['Price'] <= 20)].plot(ax=ax, 
                                 column='Price', legend=True, alpha=0.5)
geo_df[(geo_df['geometry'].apply(lambda x: x.coords[:][0][0] > -88)) 
                                 & (geo_df['Price'] > 20)].plot(ax=ax, 
                                    color='yellow', legend=True, alpha=0.5)
plt.xlabel('Longitude')
plt.ylabel('Latitude');
plt.savefig(SAVE_PATH + 'geo_res_price.png')


# restaurant crime rates
fig, ax = plt.subplots(figsize=(12,12))
chicago.plot(ax=ax, color='gray')
geo_df[(geo_df['geometry'].apply(lambda x: x.coords[:][0][0] > -88)) 
                              & (geo_df['Sum'] <= 3000)].plot(ax=ax, 
                                 column='Sum', legend=True, alpha=0.5)
geo_df[(geo_df['geometry'].apply(lambda x: x.coords[:][0][0] > -88)) 
                              & (geo_df['Sum'] > 3000)].plot(ax=ax, 
                                color='yellow', legend=True, alpha=0.5)
plt.xlabel('Longitude')
plt.ylabel('Latitude');
plt.savefig(SAVE_PATH + 'geo_res_crime.png')


# restaurant inspection
YlGrIn = ['yellow', 'lightseagreen', 'seagreen', 'royalblue', 'b', 'indigo']
fig, ax = plt.subplots(figsize=(12,12))
chicago.plot(ax=ax, color='gray')
sns.scatterplot('Longitude', 'Latitude', 
               data=geo_df[(geo_df['Inspection'] != None) & 
               (geo_df['Inspection'] !='Business Not Located')], 
               hue='Inspection', alpha=0.5, s=50, palette=YlGrIn,linewidth=0,
               hue_order=['Pass', 'Pass w/ Conditions', 'Fail', 
               'Out of Business', 'No Entry', 'Not Ready'])
plt.xlabel('Longitude')
plt.ylabel('Latitude');
plt.savefig(SAVE_PATH + 'geo_res_inspection.png')


# Restaurant area income
fig, ax = plt.subplots(figsize=(12,12))
chicago.plot(ax=ax, color='gray')
geo_df[(geo_df['geometry'].apply(lambda x: x.coords[:][0][0] > -88)) & 
                                (geo_df['Sum'] <= 3000)].plot(ax=ax, 
                                 column='Income', legend=True, alpha=0.5)
plt.xlabel('Longitude')
plt.ylabel('Latitude');
plt.savefig(SAVE_PATH + 'geo_res_income.png')

###########################
#Plot boxplots and regplot#
###########################

# income and price
plt.figure(figsize=(15, 10))
sns.regplot(data = allmenus[allmenus['Price']<=30], 
        x = 'Income', y = 'Price', scatter_kws={'alpha': 0.5,'linewidth':0},
        line_kws = {'color':'#323e46'}, ci=100)
plt.xlabel('Income', fontsize=26)
plt.ylabel('Price', fontsize=26);
plt.savefig(SAVE_PATH + 'price_income_reg.png')


# price and crime
plt.figure(figsize=(15, 10))
sns.regplot(x = 'Sum', y = 'Price', data=allmenus[allmenus['Price']<=50], 
            scatter_kws={"alpha": 0.5, 'linewidth': 0}, 
            line_kws = {'color':'#323e46'}, ci=100)
plt.xlabel('Crime Count', fontsize = 26);
plt.ylabel('Price', fontsize=26);
plt.savefig(SAVE_PATH + 'price_crime_reg.png')


temp = allmenus[(allmenus['Inspection'].isin(['Fail', 'Pass', 
       'Pass w/ Conditions', 'Out of Business'])) &(allmenus['Price'] < 40)]
dums = pd.get_dummies(temp['Inspection'])
final = pd.concat([temp, dums], axis=1)
final.drop(columns=['Inspection', 'Coordinate', 'Restaurant'], inplace=True)


# cuisine and price
fig, ax = plt.subplots(ncols=43, figsize = (20,10), sharey=True)
for idx, c in enumerate(final.columns[1:43]):
    sns.boxplot(y='Price', data=final[final[c] == 1], 
                color = 'teal', ax=ax[idx])
    ax[idx].set_xticklabels([c], rotation=90)
    if idx == 0:
        ax[idx].set_ylabel('Price', fontsize = 26)
        ax[idx].spines['right'].set_visible(False)
    else:
        ax[idx].set_ylabel('')
        ax[idx].spines['left'].set_visible(False)
        ax[idx].spines['right'].set_visible(False)
sns.boxplot(y='Price', data=final, color='yellow', ax=ax[42])
ax[42].spines['left'].set_visible(False)
ax[42].set_ylabel('')
ax[42].set_xticklabels(['Everything'], rotation=90)
plt.savefig(SAVE_PATH + 'price_cuisine_box.png')



# inspection and price
plt.figure(figsize=(12, 8))
sns.boxplot(x='Inspection', y='Price', 
            data=allmenus[allmenus['Inspection'] != 'Business Not Located'])
plt.xlabel('Inspection Result', fontsize = 26);
plt.ylabel('Price', fontsize=26);
plt.savefig(SAVE_PATH + 'price_inspect_box.png')




