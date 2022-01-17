import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 14})
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle
from matplotlib.ticker import MultipleLocator
from matplotlib.lines import Line2D

import re

from math import pi

import warnings
warnings.filterwarnings("ignore")


def confusion_matrix():
    # Wealth
    us_states = pd.read_csv("input/csv/COVID19_state.csv")
    us_states = us_states[['State', 'Gini', 'Income', 'GDP']]
    us_states.columns = ['state', 'gini', 'income', 'gdp']
    # Setup color palette
    # Color palette is created by using a screenshot from https://learnplatform.com/ and retrieving color codes via https://imagecolorpicker.com/

    lp_blue = '#0070c0'
    lp_turquoise = '#3c9e78'
    lp_green = '#70c738'
    mine_blue = '#084082'
    mine_red = '#B34F4F'
    lp_grey = '#8e9094'
    lp_grey_light = '#f0f0f0'

    # Set Color Palettes for the notebook
    lp_palette1 = [lp_blue, lp_green, lp_turquoise,  lp_grey, lp_grey_light]
    #display(sns.palplot(sns.color_palette(lp_palette1)))

    lp_cmap = LinearSegmentedColormap.from_list("", [lp_blue,  '#5cd0da',  lp_turquoise, lp_green])
    plt.cm.register_cmap("lp_cmap", lp_cmap)
    lp_cmap2 = LinearSegmentedColormap.from_list("", [lp_blue,  '#ffffff', lp_green])
    mine_cmap = LinearSegmentedColormap.from_list("", [mine_red,  '#ffffff', mine_blue])
    plt.cm.register_cmap("lp_cmap2", lp_cmap2)
    def get_lp_palette(n_colors):
        if n_colors == 2:
            lp_cmap = LinearSegmentedColormap.from_list("", [lp_blue, lp_green])
            plt.cm.register_cmap("lp_cmap0", lp_cmap)
            return sns.color_palette("lp_cmap0", n_colors=n_colors)
        elif n_colors == 3:
            lp_cmap = LinearSegmentedColormap.from_list("", [lp_blue, lp_turquoise, lp_green])
            plt.cm.register_cmap("lp_cmap1", lp_cmap)
            return sns.color_palette("lp_cmap1", n_colors=n_colors)
        else:       
            return sns.color_palette("lp_cmap", n_colors=n_colors)

    ###### districts_info ######
    districts_info = pd.read_csv("input/LearnPlatform/districts_info.csv")

    # Dropping districts with NaN states
    districts_info = districts_info[districts_info.state.notna()].reset_index(drop=True)

    # Drop column county_connections_ratio which does not contain any valuable information
    districts_info = districts_info.drop('county_connections_ratio', axis=1)

    def replace_ranges_pct(range_str):
        if range_str == '[0, 0.2[':
            return 0.1
        elif range_str == '[0.2, 0.4[':
            return 0.3
        elif range_str == '[0.4, 0.6[':
            return 0.5
        elif range_str == '[0.6, 0.8[':
            return 0.7
        elif range_str == '[0.8, 1[':
            return 0.9
        else:
            return np.nan

    districts_info['pct_black/hispanic'] = districts_info['pct_black/hispanic'].apply(lambda x: replace_ranges_pct(x))

    # Replace state strings with abbreviations
    us_state_abbrev = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District Of Columbia': 'DC',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Northern Mariana Islands':'MP',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virgin Islands': 'VI',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'
    }

    districts_info['state'] = districts_info['state'].replace(us_state_abbrev)

    ###### products_info ######
    products_info = pd.read_csv("./input/LearnPlatform/products_info.csv")

    # Convert column names to lower case and replace spaces with underscores
    products_info.columns = [f"{re.sub(' ', '_', col.lower())}" for col in products_info.columns]

    # Splitting up the primary essential functions
    products_info['primary_function_main'] = products_info['primary_essential_function'].apply(lambda x: x.split(' - ')[0] if x == x else x)
    products_info['primary_function_sub'] = products_info['primary_essential_function'].apply(lambda x: x.split(' - ')[1] if x == x else x)

    # Synchronize similar values
    products_info['primary_function_sub'] = products_info['primary_function_sub'].replace({'Sites, Resources & References' : 'Sites, Resources & Reference'})
    products_info.drop("primary_essential_function", axis=1, inplace=True)

    ###### engagement_data ######
    # temp = []

    # for district in (districts_info.district_id.unique()):
    #     df = pd.read_csv(f'./input/LearnPlatform/engagement_data/{district}.csv', index_col=None, header=0)
    #     df["district_id"] = district
    #     if df.time.nunique() == 366:
    #         temp.append(df)

    # engagement = pd.concat(temp)
    # engagement = engagement.reset_index(drop=True)
    # del temp

    # # Only consider districts with full 2020 engagement data
    # districts_info = districts_info[districts_info.district_id.isin(engagement.district_id.unique())].reset_index(drop=True)
    # products_info = products_info[products_info.lp_id.isin(engagement.lp_id.unique())].reset_index(drop=True)

    # # Only consider engagement data with lp_id in products_info
    # engagement = engagement[engagement.lp_id.isin(products_info.lp_id.unique())].reset_index(drop=True)

    # # Convert time
    # engagement.time = engagement.time.astype('datetime64[ns]')

    # # Create new features
    # engagement['cw'] = pd.DatetimeIndex(engagement['time']).week
    # engagement['weekday'] = pd.DatetimeIndex(engagement['time']).weekday

    # # Fill NaN in column engagement_index with 0
    # engagement['engagement_index'] = engagement['engagement_index'].fillna(0)

    # # Only look at engagement on weekdays
    # engagement = engagement[engagement.weekday < 5].reset_index(drop=True)

    # # Resample average data on weekly basis
    # engagement_cw = engagement.groupby(['cw', 'lp_id', 'district_id'])['pct_access', 'engagement_index'].mean().reset_index(drop=False)

    # # Covid phase:
    # # -1 : Summer break
    # # 0 : Academic year 2019/20 before COVID-19
    # # 1 : Academic year 2019/20 during COVID-19
    # # 2 : Academic year 2020/21 during COVID-19
    # engagement_cw['covid_phase'] = engagement_cw.cw.apply(lambda x: 0 if x < 10 else (2 if x > 35 else (1 if ((x>=10) & (x <=25)) else -1)))


    ###### Merge all dataframes to one big dataframe ######
    # all_data = engagement_cw.merge(products_info[['lp_id', 'product_name', 'primary_function_main', 'primary_function_sub']], on='lp_id')
    # all_data = all_data.merge(districts_info, on='district_id')

    ###### Statewise demographic data ######

    # Wealth
    us_states = pd.read_csv("input/csv/COVID19_state.csv")
    us_states['State'] = us_states['State'].replace(us_state_abbrev)
    us_states = us_states[['State', 'Gini', 'Income', 'GDP']]
    us_states.columns = ['state', 'gini', 'income', 'gdp']

    # Broadband access
    broadband_access = pd.read_csv("input/csv/broadband_access.csv")
    broadband_access = broadband_access[['state_abr', 'no_comp', 'no_internet']]
    broadband_access = broadband_access.groupby('state_abr').mean().reset_index(drop=False)
    broadband_access.columns = ['state', 'no_comp', 'no_internet']

    # Ethnicity
    demographic_data = pd.read_csv("input/csv/acs2017_county_data.csv")
    demographic_data = demographic_data[['State', 'Hispanic', 'Black']]
    demographic_data['State'] = demographic_data['State'].replace(us_state_abbrev)
    demographic_data = demographic_data.groupby('State').mean().reset_index(drop=False)
    demographic_data.columns = ['state', 'Hispanic', 'Black']
    demographic_data['pct_black/hispanic_state'] = demographic_data['Hispanic'] + demographic_data['Black']


    # https://www.edweek.org/leadership/map-coronavirus-and-school-closures-in-2019-2020/2020/03
    # https://www.edweek.org/leadership/map-where-are-schools-closed/2020/07

    us_state_policy_array = [
    ['AL', 'ordered closed', 'no order in effect'],
    ['AK', 'ordered closed', 'no order in effect'],
    ['AS', 'ordered closed', 'no order in effect'],
    ['AZ', 'ordered closed', 'some grades ordered open'],
    ['AR', 'ordered closed', 'ordered open (full-time)'],
    ['CA', 'recommended closed', 'no order in effect'],
    ['CO', 'ordered closed', 'no order in effect'],
    ['CT', 'ordered closed', 'no order in effect'],
    ['DE', 'ordered closed', 'partial closure in effect'],
    ['DC', 'ordered closed', 'partial closure in effect'],
    ['FL', 'recommended closed', 'ordered open (full-time)'],
    ['GA', 'ordered closed', 'no order in effect'],
    ['GU', 'ordered closed', 'no order in effect'],
    ['HI', 'ordered closed', 'partial closure in effect'],
    ['ID', 'recommended closed', 'no order in effect'],
    ['IL', 'ordered closed', 'no order in effect'],
    ['IN', 'ordered closed', 'no order in effect'],
    ['IA', 'ordered closed', 'ordered open (full-time)'],
    ['KS', 'ordered closed', 'ordered open (full-time)'],
    ['KY', 'recommended closed', 'no order in effect'],
    ['LA', 'ordered closed', 'no order in effect'],
    ['ME', 'recommended closed', 'no order in effect'],
    ['MD', 'ordered closed', 'no order in effect'],
    ['MA', 'ordered closed', 'ordered open (full-time)'],
    ['MI', 'ordered closed', 'no order in effect'],
    ['MN', 'ordered closed', 'no order in effect'],
    ['MS', 'ordered closed', 'no order in effect'],
    ['MO', 'ordered closed', 'no order in effect'],
    ['MT', 'n/a', 'no order in effect'],
    ['NE', 'ordered closed', 'no order in effect'],
    ['NV', 'ordered closed', 'no order in effect'],
    ['NH', 'ordered closed', 'ordered open (part-time)'],
    ['NJ', 'ordered closed', 'no order in effect'],
    ['NM', 'ordered closed', 'ordered open (part-time)'],
    ['NY', 'ordered closed', 'no order in effect'],
    ['NC', 'ordered closed', 'ordered open (part-time)'],
    ['ND', 'ordered closed', 'no order in effect'],
    ['MP', 'ordered closed', 'no order in effect'],
    ['OH', 'ordered closed', 'no order in effect'],
    ['OK', 'ordered closed', 'no order in effect'],
    ['OR', 'ordered closed', 'ordered open (part-time)'],
    ['PA', 'ordered closed', 'no order in effect'],
    ['PR', 'ordered closed', 'partial closure in effect'],
    ['RI', 'ordered closed', 'no order in effect'],
    ['SC', 'ordered closed', 'ordered open (full-time)'],
    ['SD', 'recommended closed', 'no order in effect'],
    ['TN', 'recommended closed', 'no order in effect'],
    ['TX', 'ordered closed', 'ordered open (full-time)'],
    ['UT', 'ordered closed', 'no order in effect'],
    ['VT', 'ordered closed', 'no order in effect'],
    ['VI', 'ordered closed', 'no order in effect'],
    ['VA', 'ordered closed', 'no order in effect'],
    ['WA', 'ordered closed', 'ordered open (part-time)'],
    ['WV', 'ordered closed', 'ordered open (full-time)'],
    ['WI', 'ordered closed', 'no order in effect'],
    ['WY', 'n/a', 'no order in effect'],
]

    # Create the pandas DataFrame
    us_state_policy = pd.DataFrame(us_state_policy_array, columns = ['state', 'policy_AY1920', 'policy_AY2021'])


    # Merge districts_info
    districts_info = districts_info.merge(us_state_policy, on='state')
    districts_info = districts_info.merge(us_states, on='state')
    districts_info = districts_info.merge(broadband_access, on='state')
    districts_info = districts_info.merge(demographic_data, on='state')
    districts_info = districts_info[['district_id', 'state', 'policy_AY1920', 'policy_AY2021','pct_black/hispanic', 'pct_black/hispanic_state', 'gini', 'income', 'gdp', 'no_comp', 'no_internet',]]
    cols = [c for c in districts_info.columns if c not in ['district_id', 'state', 'policy_AY1920', 'policy_AY2021','digital_pedagogical_experience_index_2']]
    corrmat = districts_info[cols].corr()
    # Visualize
    f, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))

    sns.heatmap(corrmat, annot=True, annot_kws={"size": 16, 'weight': 'bold'}, mask=np.triu(corrmat), vmin=-1, vmax=1, linewidths=1, cmap=mine_cmap,  fmt='.1f')
    labels = ['Ethnicity: % Black/Hispanic (District)', 'Ethnicity: % Black/Hispanic (State)', 'Wealth: Gini Coef. (State)','Wealth: Income (State)', 'Wealth: GDP (State)', 'Tech: No Computer Access (State)', 'Tech: No Internet Access (State)','Digital Pedagogical Experience Index']
    # ax.set_xticks(rotation=20, ha='right', fontsize = 14)
    ax.set_xticklabels(labels, rotation=20, ha='right', fontsize = 14)
    ax.set_yticklabels(labels, fontsize = 14)
    ax.add_patch(Rectangle((0, 7), 7, 1, fill=False, alpha=1, color=lp_grey, lw=5))
    plt.savefig('output/confusion_matrix.png', dpi = 300, bbox_inches='tight')
    

confusion_matrix()