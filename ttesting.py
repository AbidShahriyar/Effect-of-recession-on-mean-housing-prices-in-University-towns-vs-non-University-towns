'''
* From the Wikipedia page (https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) the
list of college towns in the United States was copied and pasted on a text file named 'university_towns.txt'.
* From the Zillow research site (https://www.zillow.com/research/data/) a csv file was downloaded with median house prices
for city levels.
* From Bureau of Economic Analysis, US Department of Commerce, (https://www.bea.gov/data/gdp/gross-domestic-product#gdp)
the GDP over time of the United States in current dollars was downloaded in the file gdplev.xls.
For this project, only the GDP data from the first quarter of 2000 onward was taken.


Hypothesis: University towns have their mean housing prices less effected by recessions.
A t-test is run to compare the ratio of the mean price of houses in university towns the quarter before the recession
starts compared to the recession bottom with the ratio of the mean price of houses in non university towns.
(price_ratio=quarter_before_recession/recession_bottom)
'''

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import re

pd.set_option('max_rows', 10000)

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the
    university_towns.txt list. The format of the DataFrame is:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ],
    columns=["State", "RegionName"]  )

    The following cleaning was done:

    1. For "State", removed characters from "[" to the end.
    2. For "RegionName", when applicable, removed every character from " (" to the end.
    3. Removed newline character '\n'.
    '''
    x = open('unitownold.txt', 'r')
    y = x.read()
    x.close()
    regex = re.compile(r'(^[A-Za-z ]+(?=\[edit\][\n]))|(^[A-Za-z]+[A-Za-z ]+(?=(\[\d+\])| \(.*[\n]))', re.M)
    results = regex.finditer(y)
    lista = []
    for result in results:
        if result.group(1):
            state = result.group(1)
        if result.group(2):
            lista.append([state, result.group(2)])
    df = pd.DataFrame(lista, columns=['State', 'RegionName'])
    return df


# This dictionary was used to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National',
          'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana',
          'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho',
          'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan',
          'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico',
          'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa',
          'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana',
          'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California',
          'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island',
          'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia',
          'ND': 'North Dakota', 'VA': 'Virginia'}


def before_recession_start():
    '''
    Returns the year and quarter of the time just before recession as a string value in a format such as 2005q3
    '''
    gdp = pd.read_excel('gdplev.xls', skiprows=7, usecols=[4, 6])
    gdp.columns = ['Quarters', 'Chained Value in 2009 Dollars']
    gdp = gdp[gdp['Quarters'] >= '2000q1']
    gdp = gdp.reset_index(drop=True)
    gdp['Chained Value in 2009 Dollars'] = gdp['Chained Value in 2009 Dollars'].apply(pd.to_numeric)
    for x in range(len(gdp) - 2):
        if (gdp.loc[x + 1, 'Chained Value in 2009 Dollars'] < gdp.loc[x, 'Chained Value in 2009 Dollars']) and (
                gdp.loc[x + 2, 'Chained Value in 2009 Dollars'] < gdp.loc[x + 1, 'Chained Value in 2009 Dollars']):
            y = gdp.loc[x, 'Quarters']
            break

    # gdp = gdp.sort_values(['Chained Value in 2009 Dollars'], ascending=False)
    return y


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a string value in a format such as 2005q3'''
    before_start = before_recession_start()
    gdp = pd.read_excel('gdplev.xls', skiprows=7, usecols=[4, 6])
    gdp.columns = ['Quarters', 'Chained Value in 2009 Dollars']
    gdp['Chained Value in 2009 Dollars'] = gdp['Chained Value in 2009 Dollars'].apply(pd.to_numeric)
    gdp = gdp[gdp['Quarters'] > before_start]
    gdp = gdp.reset_index(drop=True)
    for x in range(2, len(gdp)):
        if (gdp.loc[x - 1, 'Chained Value in 2009 Dollars'] < gdp.loc[x, 'Chained Value in 2009 Dollars']) and (
                gdp.loc[x - 2, 'Chained Value in 2009 Dollars'] > gdp.loc[x - 1, 'Chained Value in 2009 Dollars']) and (
                gdp.loc[x + 1, 'Chained Value in 2009 Dollars'] > gdp.loc[x, 'Chained Value in 2009 Dollars']):
            y = gdp.loc[x + 1, 'Quarters']
            break

    return y


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a string value in a format such as 2005q3'''
    before_start = before_recession_start()
    end = get_recession_end()
    gdp = pd.read_excel('gdplev.xls', skiprows=7, usecols=[4, 6])
    gdp.columns = ['Quarters', 'Chained Value in 2009 Dollars']
    gdp['Chained Value in 2009 Dollars'] = gdp['Chained Value in 2009 Dollars'].apply(pd.to_numeric)
    gdp = gdp[(gdp['Quarters'] > before_start) & (gdp['Quarters'] <= end)]
    gdp = gdp.reset_index(drop=True)
    gdp = gdp.loc[gdp['Chained Value in 2009 Dollars'].idxmin(), 'Quarters']
    return gdp


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean values in a dataframe. This dataframe is a
    dataframe with columns for 2000q1 through 2016q3, and contains a multi-index in the shape of ["State","RegionName"].
    '''
    df = pd.read_csv('City_Zhvi_AllHomes.csv')
    columns_to_keep = ['RegionName', 'State']
    for i in df.columns[6:]:
        if i.startswith('20'):
            columns_to_keep.append(i)
    df = df[columns_to_keep]
    df['State'] = df['State'].replace(states)
    df = df.set_index(["State", "RegionName"])
    # df = df.sort_index()
    df = df.groupby(pd.PeriodIndex(df.columns, freq='Q'), axis=1).mean()

    return df.sort_index()


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values,
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence.

    Returns the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if
    otherwise (we cannot reject the null hypothesis).
    The value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivalent to a
    reduced market loss).'''
    uni_town = get_list_of_university_towns()
    rec_beg = before_recession_start()
    rec_bot = get_recession_bottom()
    house_price = convert_housing_data_to_quarters()

    all_ratiodf = pd.DataFrame(index=house_price.index)
    all_ratiodf['ratio'] = house_price[rec_beg] / house_price[rec_bot]
    all_ratiodf = all_ratiodf.reset_index()
    unitown_ratiodf = pd.merge(all_ratiodf, uni_town, how='inner', on=['State', 'RegionName']).dropna()
    nonunitown_ratiodf = all_ratiodf[all_ratiodf.RegionName.isin(unitown_ratiodf.RegionName) == False]
    nonunitown_ratiodf = nonunitown_ratiodf.dropna()
    t, p = ttest_ind(unitown_ratiodf['ratio'], nonunitown_ratiodf['ratio'])
    different = True if p < 0.01 else False
    betters = 'university town' if unitown_ratiodf['ratio'].mean() < nonunitown_ratiodf['ratio'].mean() else 'non-university town'
    return different, p, betters

run_ttest()


'''
Output: (True, 0.002580983334909694, 'university town')

This indicates that there is actually a difference in changes of house prices during a recession in university
towns compared to non university towns.
'''