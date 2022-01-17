import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import glob
import datetime as dt
from wordcloud import WordCloud
import warnings
warnings.filterwarnings("ignore")

from scipy.stats import boxcox
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import timedelta
from sklearn.metrics import mean_squared_error

from pylab import rcParams
import statsmodels.api as sm



pio.templates.default = "plotly_white"

plt.style.use("seaborn-paper")
plt.rc("figure", autolayout=True)
plt.rc(
    "axes",
    labelweight="bold",
    labelsize="large",
    titleweight="bold",
    titlesize=16,
    titlepad=10,
)


def count_plot(dataframe, feature, color='#084082'):
    if len(feature)==1 and dataframe[feature[0]].nunique()<6:
        fig = px.bar(x=dataframe[feature[0]].value_counts().index, y=dataframe[feature[0]].value_counts().values)
        #fig.update_layout(font_family="Comic Sans MS")
        fig.update_xaxes(tickangle=270, title=None, tickfont_size=16)
        fig.update_yaxes(title="Counts")
        return fig
    else:
        fig = px.bar(y=dataframe[feature[0]].value_counts().index, x=dataframe[feature[0]].value_counts().values, orientation="h")
        #fig.update_layout(font_family="Comic Sans MS")
        fig.update_xaxes(title="Counts", tickfont_size=14)
        fig.update_yaxes(title=None)
        return fig
         
def bar_plot(dataframe, feature1, feature2):
    if len(feature2)>1:
        fig = make_subplots(rows=1, cols=len(feature2), subplot_titles=feature2)
        for i in range(len(feature2)):
            fig.add_trace(go.Bar(x=dataframe[feature1[0]], y=dataframe[feature2[i]], name=feature2[i]), row=1, col=i+1)
        fig.update_layout( showlegend=False, margin=dict(l=0, r=0, t=100, b=50), height=400)
        return fig

def bar_plot_day2week(dataframe, feature1, feature2):
    colors = ['#9FC1D1',] * 7
    colors[5] = '#904B53'
    colors[6] = '#904B53'

    if len(feature2)>1:
        fig = make_subplots(rows=1, cols=len(feature2), subplot_titles=feature2)
        week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for i in range(len(feature2)):
            fig.add_trace(go.Bar(x=week , y=dataframe[feature2[i]], name=feature2[i], marker_color=colors), row=1, col=i+1)
        fig.update_layout( showlegend=False, margin=dict(l=0, r=0, t=100, b=50), height=400)
        return fig

def pie_plot(dataframe, feature):
    fig = go.Figure()
    fig.add_trace(go.Pie(values=dataframe[feature].value_counts().values, labels=dataframe[feature].value_counts().index,
                        pull=[0,0.1,0,0.1],textinfo='percent+value'))
    fig.update_layout( margin=dict(t=100, b=50))
    return fig

def map_plot(dataframe, location, color, hover):
    fig = px.choropleth(data_frame=dataframe, locations=location, locationmode="USA-states",
                    color=color, scope="usa", hover_name=hover, color_continuous_scale="viridis_r")
    fig.update_layout()
    return fig

def path_plot(dataframe, path, values, plot_type):
    if plot_type=="treemap":
        fig = px.treemap(data_frame=dataframe, path=path, values=values,
                       color_discrete_sequence=px.colors.qualitative.G10)
        fig.update_layout( font_size=16, margin=dict(t=50, b=0))
        return fig
    elif plot_type=="sunburst":
        fig = px.sunburst(data_frame=dataframe, path=path, values=values,
                       color_discrete_sequence=px.colors.qualitative.G10)
        fig.update_layout( font_size=16, margin=dict(t=50, b=0))
        return fig

def time_plot(df, factor, label):
    
    for i in ["pct_access","engagement_index"]:
        fig = px.line(data_frame=df, x="week", y=i, color=factor)
        fig.update_layout(title=dict(text="<b>"+i+" - "+factor+" wise - "+label, x=0.5, font_size=20), height=300, margin=dict(b=0))
        fig.update_xaxes(title=None)
        fig.update_yaxes(title=None)
        fig.show()

def time_plot_mine(df):
    print(df)
        
def comparison_bar_plot(df):
    fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01,
                    subplot_titles=["<b>Based on PCT Access", "<b>Based on Enagagement Index"])

    fig.add_trace(go.Bar(x=df["pct_access"], y=df["Product Name"], 
                         text=df.pct_rank, textposition="outside",orientation="h"), row=1, col=1)
    fig.add_trace(go.Bar(x=df.engagement_index, y=df["Product Name"], 
                         text=df.engagement_rank, textposition="outside", orientation="h"), row=1, col=2)
    fig.add_annotation(x=250000000, y=3, font_size=16,
                text="<b>Number</b> over the Bars <br>depicts their <b>Overall Rank</b> in<br> Products List", 
                       row=1, col=2, showarrow=False)
    return fig

def month_map_comparison(df, name):
    
    months_map = {1:"January",2:"February",3:"March",4:"April",
              5:"May",6:"June",7:"July",8:"August",9:"September",
              10:"October",11:"November",12:"December"}
    
    temp = df.copy()
    temp["month"] = temp.time.dt.month
    temp = temp.groupby(["state","state_code","month"])[["pct_access","engagement_index"]].mean().reset_index()
    temp["Month_2020"] = temp.month.map(months_map)
    
    
    pct_min = temp.pct_access.min()
    pct_max = np.round(temp.pct_access.max(),0)
    #pct_access over the time
    fig = px.choropleth(data_frame=temp, locations="state_code", locationmode="USA-states",
                        color="pct_access", scope="usa",
                        color_continuous_scale="Portland_r", animation_frame="Month_2020", hover_name="state", \
                        range_color=[pct_min, pct_max])
    fig.update_layout(
                      title=dict(text="<b>PCT Access over Time - "+name, font_size=20, x=0.5))
    fig.show()

    
    eng_min = temp.engagement_index.min()
    eng_max = np.round(temp.engagement_index.max(),0)
    # Enagagement Index over the time
    fig = px.choropleth(data_frame=temp, locations="state_code", locationmode="USA-states",
                        color="engagement_index", scope="usa",
                        color_continuous_scale="Portland_r", animation_frame="Month_2020", hover_name="state",
                        range_color=[eng_min, eng_max])
    fig.update_layout( 
                      title=dict(text="<b>Engagement Index over Time - "+name, font_size=20, x=0.5))
    fig.show()
    
def time_analysis(df, title):
    df2 = pd.Series(boxcox(df, lmbda=0), index=df.index)
    
    train = df2.iloc[:301]
    test = df2.iloc[301:]
    
    model = SARIMAX(train, order=(1,1,1), seasonal_order=(1,1,1,14), exog=holiday.iloc[:301]).fit()
    
    predictions = df.copy()
    predictions["forecast_box_cox"] = model.predict(df.index.max(), holiday.index.max(),
                                                    exog=holiday.loc[test.index.min():holiday.index.max()])
    
    predictions["forecast"] = np.exp(predictions["forecast_box_cox"])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df.values, name="Original"))
    fig.add_trace(go.Scatter(x=predictions["forecast"].index, y=predictions["forecast"].values, name="Forecast",
                            line_color="lightblue"))
    fig.update_layout(title=dict(text=title, font_size=20, x=0.5, font_family="Comic Sans MS"),
                      margin=dict(b=20, t=50, r=0), height=400)
    fig.show()

def timePlot(data, type, range):
    # import matplotlib.pyplot as plt
    # import geopandas
    # states = geopandas.read_file('archive/us_covid19_daily.csv')
    # f = states.plot()
    # f.figure.savefig("output/map.png", dpi=300)



    import numpy as np
    import matplotlib.pyplot as plt
    # from mpl_toolkits.basemap import Basemap
    from matplotlib.colors import rgb2hex
    from matplotlib.patches import Polygon


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

    # Setup color palette
    # Color palette is created by using a screenshot from https://learnplatform.com/ and retrieving color codes via https://imagecolorpicker.com/

    lp_blue = '#0070c0'
    lp_turquoise = '#3c9e78'
    lp_green = '#70c738'
    lp_grey = '#8e9094'
    lp_grey_light = '#f0f0f0'

    # Set Color Palettes for the notebook
    lp_palette1 = [lp_blue, lp_green, lp_turquoise,  lp_grey, lp_grey_light]
    #display(sns.palplot(sns.color_palette(lp_palette1)))

    lp_cmap = LinearSegmentedColormap.from_list("", [lp_blue,  '#5cd0da',  lp_turquoise, lp_green])
    plt.cm.register_cmap("lp_cmap", lp_cmap)
    lp_cmap2 = LinearSegmentedColormap.from_list("", [lp_blue,  '#ffffff', lp_green])
    plt.cm.register_cmap("lp_cmap2", lp_cmap2)


    ###### districts_info ######
    districts_info = pd.read_csv("./input/LearnPlatform/districts_info.csv")

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
    temp = []

    for district in (districts_info.district_id.unique()):
        df = pd.read_csv(f'./input/engagement_data/{district}.csv', index_col=None, header=0)
        df["district_id"] = district
        if df.time.nunique() == 366:
            temp.append(df)

    engagement = pd.concat(temp)
    engagement = engagement.reset_index(drop=True)
    del temp

    # Only consider districts with full 2020 engagement data
    districts_info = districts_info[districts_info.district_id.isin(engagement.district_id.unique())].reset_index(drop=True)
    products_info = products_info[products_info.lp_id.isin(engagement.lp_id.unique())].reset_index(drop=True)

    # Only consider engagement data with lp_id in products_info
    engagement = engagement[engagement.lp_id.isin(products_info.lp_id.unique())].reset_index(drop=True)

    # Convert time
    engagement.time = engagement.time.astype('datetime64[ns]')

    # Create new features
    engagement['cw'] = pd.DatetimeIndex(engagement['time']).week
    engagement['weekday'] = pd.DatetimeIndex(engagement['time']).weekday

    # Fill NaN in column engagement_index with 0
    engagement['engagement_index'] = engagement['engagement_index'].fillna(0)

    # Only look at engagement on weekdays
    engagement = engagement[engagement.weekday < 5].reset_index(drop=True)

    # Resample average data on weekly basis
    engagement_cw = engagement.groupby(['cw', 'lp_id', 'district_id'])['pct_access', 'engagement_index'].mean().reset_index(drop=False)

    # Covid phase:
    # -1 : Summer break
    # 0 : Academic year 2019/20 before COVID-19
    # 1 : Academic year 2019/20 during COVID-19
    # 2 : Academic year 2020/21 during COVID-19
    engagement_cw['covid_phase'] = engagement_cw.cw.apply(lambda x: 0 if x < 10 else (2 if x > 35 else (1 if ((x>=10) & (x <=25)) else -1)))


    ###### Merge all dataframes to one big dataframe ######
    all_data = engagement_cw.merge(products_info[['lp_id', 'product_name', 'primary_function_main', 'primary_function_sub']], on='lp_id')
    all_data = all_data.merge(districts_info, on='district_id')



    ###### us_covid19_daily ######

    us_covid = pd.read_csv("./archive/us_covid19_daily.csv")
    us_covid['date'] = pd.to_datetime(us_covid.date, format = '%Y%m%d')
    us_covid['cw'] = pd.DatetimeIndex(us_covid['date']).week
    print(us_covid['cw'])

    us_covid = us_covid.sort_values(by='date')
    us_covid['new_cases'] = us_covid['positive'].diff()

    us_covid = us_covid.groupby('cw')[['new_cases']].mean().reset_index(drop=False)

    # Visualize
    virtual_classroom_lp_id = products_info[products_info.primary_function_sub == 'Virtual Classroom'].lp_id.unique()

    engagement_sum = engagement_cw[engagement_cw.lp_id.isin(virtual_classroom_lp_id)].groupby(['cw', 'district_id']).pct_access.sum().to_frame().reset_index()

    # visualize 
    f, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 6))
    temp = engagement_sum.groupby('cw').pct_access.mean().to_frame().reset_index(drop=False)
    sns.lineplot(x=us_covid.cw, y=us_covid.new_cases, color= '#aaaaaa', label = 'Avg. Weekly New Covid Cases', legend=False, linewidth=1)
    ax.lines[0].set_linestyle("--")
    ax.set_ylim([0, 200000])  
    

    ax2 = ax.twinx()
    locales = ['City', 'Town', 'Suburb', 'Rural']
    colors=['#084082', '#B4C0D4', '#E0B7B5', '#B34F4F']
    if type=='pct_access':
        sns.lineplot(x=data.week, y=data[data.locale==locales[0]].pct_access, ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[0], legend=False, linewidth=3)
        sns.lineplot(x=data.week, y=data[data.locale==locales[1]].pct_access, ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[1], legend=False, linewidth=3)
        sns.lineplot(x=data.week, y=data[data.locale==locales[2]].pct_access, ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[2], legend=False, linewidth=3)
        sns.lineplot(x=data.week, y=data[data.locale==locales[3]].pct_access, ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[3], legend=False, linewidth=3)
    elif type == 'engagement_index':
        sns.lineplot(x=data.week, y=data[data.locale==locales[0]].engagement_index, ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[0], legend=False, linewidth=3)
        sns.lineplot(x=data.week, y=data[data.locale==locales[1]].engagement_index, ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[1], legend=False, linewidth=3)
        sns.lineplot(x=data.week, y=data[data.locale==locales[2]].engagement_index, ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[2], legend=False, linewidth=3)
        sns.lineplot(x=data.week, y=data[data.locale==locales[3]].engagement_index, ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[3], legend=False, linewidth=3)
    
    plt.legend(labels=locales)
    ax2.set_ylim([0, range])  
    ax2.set_xlim([1, 53]) 

    # https://www.mykidstime.com/school/here-are-the-school-holidays-2019/
    # https://www.edarabia.com/school-holidays-united-states/
    # Mid Winter Break
    ax2.add_patch(Rectangle((7.5, 0), 1, range, fill=True, alpha=0.2, color='#9FC1D1', lw=0))
    ax2.annotate('Mid Winter Break', xy=(8, range/2), fontsize=14, color='#999999', rotation=90, va='center', ha='center')

    # Spring Break
    ax2.add_patch(Rectangle((16.5, 0), 1, range, fill=True, alpha=0.2, color='#9FC1D1', lw=0))
    ax2.annotate('Spring Break', xy=(17, range/2), fontsize=14, color='#999999', rotation=90, va='center', ha='center')

    # Summer Break
    ax2.add_patch(Rectangle((25.5, 0), 7, range, fill=True, alpha=0.2, color='#9FC1D1', lw=0))
    ax2.annotate('Summer Break', xy=(29, range/2), fontsize=14, color='#999999', rotation=90, va='center', ha='center')

    # Thanksgiving
    ax2.add_patch(Rectangle((47.5, 0), 1, range, fill=True, alpha=0.2, color='#9FC1D1', lw=0))
    ax2.annotate('Thanksgiving', xy=(48, range/2), fontsize=14, color='#999999', rotation=90, va='center', ha='center')

    # Christmas
    ax2.add_patch(Rectangle((51.5, 0), 3, range, fill=True, alpha=0.2, color='#9FC1D1', lw=0))
    ax2.annotate('Christmas', xy=(52.5, range/2), fontsize=14, color='#999999', rotation=90, va='center', ha='center')

    ax.set_xlabel('Calendar Week 2020',fontsize=14 , fontweight='bold')
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax2.set_ylabel(type, color='#000000', fontweight='bold')
    ax2.tick_params(axis='y', colors = '#000000', direction='in')

    ax.set_ylabel('Average Daily New Covid-19 Cases', color='#aaaaaa')
    ax.tick_params(axis='y', colors = '#aaaaaa', direction='in')
    ax.tick_params(axis='x', direction='in')
    plt.savefig('output/locale_'+type+'.png', dpi=300,  bbox_inches='tight')



# function for extracting the average of the values from the ranges
def avg_ranges(x):
    return np.array(str(x).strip("[").split(",")).astype(float).mean()

def sub_category(x):
    a = str(x).split("-")
    if len(a)<2:
        return x
    else:
        return "-".join(a[1:])

