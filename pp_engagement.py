import pandas as pd
def timePlot(data, type, target, range, target_list, legend_list, fig_name, colors):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import rgb2hex
    from matplotlib.patches import Polygon
    import numpy as np # linear algebra
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

    
    
    lp_cmap = LinearSegmentedColormap.from_list("", ['#0070c0',  '#5cd0da',  '#3c9e78', '#70c738'])
    plt.cm.register_cmap("lp_cmap", lp_cmap)
    lp_cmap2 = LinearSegmentedColormap.from_list("", ['#0070c0',  '#ffffff', '#70c738'])
    plt.cm.register_cmap("lp_cmap2", lp_cmap2)

    ###### us_covid19_daily ######
    us_covid = pd.read_csv("./input/csv/us_covid19_daily.csv")
    us_covid['date'] = pd.to_datetime(us_covid.date, format = '%Y%m%d')
    us_covid['cw'] = pd.DatetimeIndex(us_covid['date']).week
    us_covid = us_covid.sort_values(by='date')
    us_covid['new_cases'] = us_covid['positive'].diff()
    us_covid = us_covid.groupby('cw')[['new_cases']].mean().reset_index(drop=False)

    # visualize 
    f, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 6))
    sns.lineplot(x=us_covid.cw, y=us_covid.new_cases, color= '#aaaaaa', label = 'Avg. Weekly New Covid Cases', legend=False, linewidth=1)
    ax.lines[0].set_linestyle("--")
    ax.set_ylim([0, 200000])  
    

    ax2 = ax.twinx()

    # locales = ['[4000, 6000[', '[6000, 8000[','[8000, 10000[','[10000, 12000[', '[12000, 14000[', '[14000, 16000[', '[16000, 18000[','[18000, 20000[','[20000, 22000[', '[22000, 24000[', '[24000, 26000[', '[32000, 34000[']
    
    if type=='pct_access':
        sns.lineplot(x=data.week, y=data[data[target]==target_list[0]].pct_access, ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[0], legend=False, linewidth=3)
        sns.lineplot(x=data.week, y=data[data[target]==target_list[1]].pct_access, ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[1], legend=False, linewidth=3)
        sns.lineplot(x=data.week, y=data[data[target]==target_list[2]].pct_access, ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[2], legend=False, linewidth=3)
        sns.lineplot(x=data.week, y=data[data[target]==target_list[3]].pct_access, ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[3], legend=False, linewidth=3)
    elif type == 'engagement_index':
        sns.lineplot(x=data.week, y=data[data[target]==target_list[0]].engagement_index,  ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[0],  legend=False, linewidth=3)
        sns.lineplot(x=data.week, y=data[data[target]==target_list[1]].engagement_index,  ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[1],  legend=False, linewidth=3)
        sns.lineplot(x=data.week, y=data[data[target]==target_list[2]].engagement_index,  ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[2],  legend=False, linewidth=3)
        sns.lineplot(x=data.week, y=data[data[target]==target_list[3]].engagement_index,  ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[3],  legend=False, linewidth=3)
        
        # sns.lineplot(x=data.week, y=data[data.pp_total_raw==target_list[0]].engagement_index,  ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[0],  legend=False, linewidth=3)
        # sns.lineplot(x=data.week, y=data[data.pp_total_raw==target_list[1]].engagement_index,  ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[1],  legend=False, linewidth=3)
        # sns.lineplot(x=data.week, y=data[data.pp_total_raw==target_list[2]].engagement_index,  ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[2],  legend=False, linewidth=3)
        # sns.lineplot(x=data.week, y=data[data.pp_total_raw==target_list[3]].engagement_index,  ax=ax2,  label=f'Virtual Classroom pct_access', color= colors[3],  legend=False, linewidth=3)
        
    
    plt.legend(labels=legend_list)
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
    plt.savefig('output/pdf/'+fig_name+'.pdf', dpi=300,  bbox_inches='tight')
    plt.savefig('output/png/'+fig_name+'.png', dpi=300,  bbox_inches='tight')
    print('Figure '+fig_name+'.pdf has been generated!')



# colors = ['#A6CEE3', '#1F78B4', '#B2DF8A', '#33A02C', '#FDBF6F', '#FB7F01', '#CAB2D7', '#6A3D9A', '#FFFD99', '#B15928', '#E31A1D', '#FB9A99']
# colors=['#084082', '#B4C0D4', '#E0B7B5', '#B34F4F']




## Week 2 Engagement for each pp_total_raw (4 intervals)
temp = pd.read_csv('input/csv/pp_engage_4.csv')
pp_list = [0, 1, 2, 3]
legend_list = ['4K-10K', '10K-16K', '16K-22K', '22K-34K']
colors=['#084082', '#B4C0D4', '#CAB2D7', '#6A3D9A']
timePlot(temp, 'engagement_index','pp_total_raw', 1300 , pp_list, legend_list, 'week2engagement_eachPP', colors)

## Week 2 pct_access for each pp_total_raw (4 intervals)
temp = pd.read_csv('input/csv/pp_engage_4.csv')
pp_list = [0, 1, 2, 3]
legend_list = ['4K-10K', '10K-16K', '16K-22K', '22K-34K']
colors=['#084082', '#B4C0D4', '#CAB2D7', '#6A3D9A']
timePlot(temp, 'pct_access','pp_total_raw', 3, pp_list, legend_list, 'week2pctAccess_eachPP', colors)


## Week 2 Engagement for each locale ('City', 'Town', 'Suburb', 'Rural')
temp = pd.read_csv('input/csv/localewise.csv')
locales = ['City', 'Town', 'Suburb', 'Rural']
colors=['#084082', '#B4C0D4', '#E0B7B5', '#B34F4F']
timePlot(temp, 'engagement_index', 'locale',  550 , locales, locales, 'week2engagement_locale', colors)

## Week 2 pct_access for each locale ('City', 'Town', 'Suburb', 'Rural')
temp = pd.read_csv('input/csv/localewise.csv')
locales = ['City', 'Town', 'Suburb', 'Rural']
colors=['#084082', '#B4C0D4', '#E0B7B5', '#B34F4F']
timePlot(temp, 'pct_access', 'locale',  2.5 , locales, locales, 'week2pctAccess_locale', colors)
