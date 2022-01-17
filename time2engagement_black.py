import pandas as pd
import numpy as np
import datetime
import glob
import copy
import os

from plotly import subplots
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objects as go
import plotly.express as px

import gc

import warnings  
warnings.filterwarnings('ignore')
init_notebook_mode(connected=True)

from IPython.core.display import display, HTML, Javascript

# define the colour palette to be used
palette_darkgrey = "#084082"
palette_silver = "#cacaca"
palette_red = "#be4B53"
palette_blue = "#1866AC"
palette_platinum = "#E3E4E5"

palette_grey2 = "#3787C1"
palette_grey3 = "#5DA4D0"
palette_grey4 = "#a0C2DE"



def annotation_helper(fig, texts, x, y, line_spacing, align="left", bgcolor="rgba(0,0,0,0)", borderpad=0, ref="axes", width=100):
    
    is_line_spacing_list = isinstance(line_spacing, list)
    
    total_spacing = 0
    
    for index, text in enumerate(texts):
        if is_line_spacing_list and index!= len(line_spacing):
            current_line_spacing = line_spacing[index]
        elif not is_line_spacing_list:
            current_line_spacing = line_spacing
        
        fig.add_annotation(dict(
            x= x,
            y= y - total_spacing,
            width = width,
            showarrow=False,
            text= text,
            bgcolor= bgcolor,
            align= align,
            borderpad=4,
            xref= "x" if ref=="axes" else "paper",
            yref= "y" if ref=="axes" else "paper"
        ))
        
        total_spacing  += current_line_spacing

# fig = go.Figure()
# text = [
#         "<b style='color:%s; font-family:Tahoma; font-size:12px'>0-20%%</b>" % (palette_red),
#         "<b style='color:%s; font-family:Tahoma; font-size:12px'>Hispanic/black</b>" % (palette_red),
#         "<b style='color:%s; font-family:Tahoma; font-size:12px'>students</b>" % (palette_red),
#         "116 districts" 
#     ]
# annotation_helper(fig, text, datetime.date(2021, 2, 12), 150, [25,30,35])
# os._exit()

# Helper functions to assign the values for high_hispanic_black_pct        
def assign_high_hispanic_black_pct(x):
    pct = x["pct_black_hispanic"]
    if pct >= 0.4:
        return True
    elif pct < 0.4:
        return False
    else:
        return np.NaN
    
def assign_high_hispanic_black_pct_categorical(x):
    pct = x["pct_black/hispanic"]
    if pct in ["[0.4, 0.6[", "[0.6, 0.8[", "[0.8, 1["]:
        return True
    elif pct in  ["[0, 0.2[", "[0.2, 0.4["]:
        return False
    else:
        return np.NaN

def time2engagement(target, output_name, annotation):

    engagement_data = []
    engagement_df = pd.read_csv('./input/csv/engagement_df.csv')
    districts_info = pd.read_csv("./input/LearnPlatform/districts_info.csv")
    products_info = pd.read_csv("./input/LearnPlatform/products_info.csv")

    engagement_districts_merged = pd.merge(engagement_df, districts_info,how="left", on="district_id")
    del engagement_df
    gc.collect()

    engagement_districts_products_merged = pd.merge(engagement_districts_merged, products_info, how="left", left_on="lp_id", right_on="LP ID")
    del engagement_districts_merged
    gc.collect()

    engagement_full = engagement_districts_products_merged[engagement_districts_products_merged["state"].notnull()]
    del engagement_districts_products_merged

    del engagement_data
    gc.collect()

    # engagement_by_hispanic_black = engagement_full[engagement_full["state"].notnull()].groupby(["pct_black/hispanic","time"])["engagement_index"].mean().reset_index()
    # engagement_by_reduce_free = engagement_full[engagement_full["state"].notnull()].groupby(["pct_free/reduced","time"])["engagement_index"].mean().reset_index()
    
    engagement_by_target = engagement_full[engagement_full["state"].notnull()].groupby([target,"time"])["engagement_index"].mean().reset_index()
    moving_average_window = 14;

    layout = dict(
        margin = dict(l=80, r=80, t=60, b=60),
        xaxis = dict(showline=True, linewidth=1, linecolor=palette_darkgrey, dtick="M1",tickformat="%b\n%Y"),
        yaxis = dict(title="Mean of Engagement Index",showline=False, showgrid=True, gridwidth=1, gridcolor='#ddd', linecolor=palette_darkgrey),
        showlegend = False,
        hovermode="x unified",
        width = 800,
        height = 550,
        plot_bgcolor= "#fff",
        hoverlabel=dict(
            bgcolor="white",
            font_size=12
        )
    )

    fig = go.Figure(layout=layout)

    engagement_02_04= engagement_by_target[engagement_by_target[target]=="[0.2, 0.4["]
    fig.add_trace(go.Scatter(
                        x=engagement_02_04["time"], 
                        y= engagement_02_04["engagement_index"].rolling(moving_average_window).mean(),
                        mode='lines',
                        line= dict(color=palette_grey4, width=1.5),
                        name='  20-40%'))

    engagement_04_06= engagement_by_target[engagement_by_target[target]=="[0.4, 0.6["]
    fig.add_trace(go.Scatter(
                        x=engagement_04_06["time"], 
                        y= engagement_04_06["engagement_index"].rolling(moving_average_window).mean(),
                        mode='lines',
                        line= dict(color=palette_grey3, width=1.5),
                        name='  40-60%'))

    engagement_06_08= engagement_by_target[engagement_by_target[target]=="[0.6, 0.8["]
    fig.add_trace(go.Scatter(
                        x=engagement_06_08["time"], 
                        y= engagement_06_08["engagement_index"].rolling(moving_average_window).mean(),
                        mode='lines',
                        line= dict(color=palette_grey2, width=1.5),
                        name='  60-80%'))

    engagement_08_10= engagement_by_target[engagement_by_target[target]=="[0.8, 1["]
    fig.add_trace(go.Scatter(
                        x= engagement_08_10["time"],
                        y= engagement_08_10["engagement_index"].rolling(moving_average_window).mean(),
                        mode='lines',
                        line= dict(color=palette_darkgrey, width=1.8),
                        name='  80-100%'))

    engagement_00_02= engagement_by_target[engagement_by_target[target]=="[0, 0.2["]


    # draws the filled in learning gap
    fig.add_trace(go.Scatter(
                        x=engagement_00_02["time"], 
                        y= engagement_00_02["engagement_index"].rolling(moving_average_window).mean(),
                        mode='lines',
                        line= dict(color="#ccc", width=0),
                        fill="tonexty",                                                                                              
                        hoverinfo='none', 
    ))

    fig.add_trace(go.Scatter(
                        x=engagement_00_02["time"], 
                        y= engagement_00_02["engagement_index"].rolling(moving_average_window).mean(),
                        mode='lines',
                        line= dict(color=palette_red, width=3),
                        name='     0-20%'))



    text = [
        "<b style='color:%s; font-family:Tahoma; font-size:12px'>80-100%% </b>" % (palette_darkgrey),
        "<b>Free/reduced-price lunch students</b>",
        # "8 districts" 
    ]

    annotation_helper(fig, text, datetime.date(2020, 10, 1), 500, [25,30], width=250)


    text = [
        "<b style='color:%s; font-family:Tahoma; font-size:12px'>0-20%%</b>" % (palette_red),
        "<b style='color:%s; font-family:Tahoma; font-size:12px'>Free/reduced-price lunch students</b>" % (palette_red),
        # "<b style='color:%s; font-family:Tahoma; font-size:12px'>students</b>" % (palette_red),
        # "116 districts" 
    ]

    annotation_helper(fig, text, datetime.date(2020, 11, 7), 50, [25, 30], width=250)


    text = [
        "<b style='color:%s; font-family:Tahoma; font-size:12px'>20-40%%</b>" % (palette_grey4),
        "<b style='color:%s; font-family:Tahoma; font-size:12px'>40-60%%</b>" % (palette_grey3),
        "<b style='color:%s; font-family:Tahoma; font-size:12px'>60-80%%</b>" % (palette_grey2),
    ]

    annotation_helper(fig, text, datetime.date(2020, 11, 5), 175, [25,30], width=50, bgcolor="rgba(255,255,255,0.7)")


    
    fig.write_image('output/png/'+output_name+'.png',scale=1, width=800, height=550)
    fig.write_image('output/pdf/'+output_name+'.pdf',scale=1, width=800, height=550)
    print('Figure '+output_name+'.pdf has been generated!')

# time2engagement('pct_black/hispanic', 'time2engagement_black', 'Hispanic/black students')
time2engagement('pct_free/reduced', 'time2engagement_lunch', 'Free/reduced-price lunch students')