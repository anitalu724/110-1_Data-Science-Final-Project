import pandas as pd
import os
import numpy as np
from plot import *

district_info = pd.read_csv('input/newLearnPlatform/new_districts.csv')
products_info = pd.read_csv('input/newLearnPlatform/new_products.csv')
pp_total_raw_dict = {'[4000, 6000[':0, '[6000, 8000[':0, '[8000, 10000[':0,
                     '[10000, 12000[':1, '[12000, 14000[':1, '[14000, 16000[':1,
                     '[16000, 18000[':2, '[18000, 20000[':2, '[20000, 22000[':2,
                     '[22000, 24000[':3, '[24000, 26000[':3, '[32000, 34000[':3}


engagement_data = pd.read_csv('output/csv/engagement.csv')
engagement_data["week"] = pd.to_datetime(engagement_data.time).dt.weekofyear
engagement_data["day_of_week"] = pd.to_datetime(engagement_data.time).dt.dayofweek



def getEngagementIndex(map_col_name, map_dict, target):
    new_district_info = district_info.replace({map_col_name:map_dict})
    df = pd.merge(engagement_data, new_district_info, on="district_id", how="inner")
    df = pd.merge(df, products_info, left_on="lp_id", right_on="LP ID", how="inner")
    temp = df.groupby([target,"week"])[["pct_access","engagement_index"]].mean().reset_index()
    temp.to_csv('input/csv/pp_engage_4.csv', index = False)
    


getEngagementIndex('pp_total_raw', pp_total_raw_dict, 'pp_total_raw')