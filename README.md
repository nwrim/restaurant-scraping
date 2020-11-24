# CAPP30122 (Computer Science with Applications 2) Final Project

## Restaurant Price, Inspection Performance, Area Income, and Crime Rates
## Nak Won Rim, Anqi Hu, Chia-yun Chang

# Libraries

For required libraries: see requirements.txt. 
All libraries can be installed with requirements.txt. 
To install, run pip install -r requirements.txt

# Software Structure

0. `mapping_dict.py`: This module scrapes the cuisine information from allmenus.com. This module was
used for some inital data exploration to group some cuisines together. Written by Nak Won Rim.
1. `scraper.py` : This module contains a Scraper object that scrapes all available restaurant information in Chicago from allmenus.com. You can specifically choose cuisines to scrape, or scrape all available cuisine using this object. Restaurant name, address, coordinate, cusine category (changed into dummy variable) and median price of each menu sections are collected. Written by Nak Won Rim.
2. `tract_income.py` : This module obtains census tract information from the US Census Geocoder with street address. Then, the tract number is mapped to the tract level income dataset for the 2017 median Household Income. Written by Anqi Hu.
3. `inspection.py` : This module uses street address to link restaurant information to the Chicago food inspection data by Jaro-Winkler distance. Inspection-level addresses are used to obtain the latest inspection result. Written by Anqi Hu.
4. `count_crime.py` : This module contains a function that counts occurrences/type of crimes that happened within a given distance of a restaurant. There’s is a function to calculate distances between two given longitude and latitudes. Crimes are counted within a vicinity of 0.8 km. Written by Chia-yun Chang
5. `go.py` (Takes about 11 hours to finish running; see test.py): This module uses `scraper.py`, `tract_income.py`, `inspection.py`, `count_crime.py` to generate the final dataset as a pickle file. Written by Nak Won Rim.
6. `test.py` : This module is equivalent to go.py, but runs on only a small subset (1 cuisine) so that people can check the go.py works. Written by Nak Won Rim.
7. `visualize.py` : This module contains the code to generate the graphs from the final dataset. We use Chicago shape files and geopandas to plot price, crime rates, area income, and inspection results by restaurant location. Statistical distribution plots (boxplots and scatterplots with regression) are plotted to describe the dataset as well. Written by Nak Won Rim, Anqi Hu, and Chia-yun Chang.
8. `regression.py`: This module takes in the cleaned dataset and outputs an OLS regression summary on  food prices, using all available variables for cuisine categories, crime types and inspection results. Written by Nak Won Rim, Anqi Hu, and Chia-yun Chang.

**Note that we are not uploading any final scraped data or downloaded data in this repository in case of copyright issues, etc**.

# Results and Visualizations

Please refer to [https://nwrim.github.io/posts/2020/03/CAPP30122/](https://nwrim.github.io/posts/2020/03/CAPP30122/) for results and visualizations.