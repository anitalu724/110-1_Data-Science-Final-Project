# import pandas as pd
# import numpy as np
# from plot import *
# import os

# districts = pd.read_csv("./input/LearnPlatform/districts_info.csv")

# # importing household income table from below url
# household_income = pd.read_html("https://fred.stlouisfed.org/release/tables?eid=259515&rid=249")[0]
# # extracting useful data
# household_income.columns = ["unknown","state","Income","preceding_period","year_ago_period"]    #renaming the columns
# household_income.drop(["unknown","preceding_period","year_ago_period"], axis=1, inplace=True)    #removing not reuired features
# household_income.replace("District of Columbia","District Of Columbia", inplace=True)

# # Poverty level of States - using information from wikipedia - using below url
# poverty = pd.read_html("https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_poverty_rate")[1]
# # Extracting useful columns from the poverty and cleaning it
# poverty.columns = ["rank","state","poverty_rate","poverty_rate_2014","poverty_measure"]    #renaming the columns
# poverty.drop(["rank","poverty_rate_2014","poverty_measure"], axis=1, inplace=True)        #droppimg not so reuired columns
# poverty.replace("District of Columbia","District Of Columbia", inplace=True)
# # cleaning the poverty percentage column
# poverty.poverty_rate = poverty.poverty_rate.apply(lambda x: float(x.split("%")[0]))    #cleaning the poverty_rate column


# districts = pd.merge(districts, poverty, how="left", on="state")      # merging poverty with districts
# districts = pd.merge(districts, household_income, how="left", on="state")    #merging household income with districts
# # Data cleaning 
# districts.dropna(axis=0, subset=["state"], inplace=True)
# # checking the distribution of county_connections_ratio
# districts.county_connections_ratio.value_counts()
# # dropping connections columns
# districts.drop(["county_connections_ratio"], axis=1, inplace=True)
# #pct_free_reduced
# districts[districts["pct_free/reduced"].isnull()].state.value_counts()

# # # Average Household Income of States of USA
# # USA_household_income = districts.Income.mean()
# # # Average poverty level of States of USA
# # USA_poverty_line = districts.poverty_rate.mean()
# # imputing missing values in State column
# districts.loc[districts.state=="Massachusetts", "pct_free/reduced"] = districts.loc[districts.state=="Massachusetts", "pct_free/reduced"].fillna("[0.2, 0.4[")
# districts.loc[districts.state=="District Of Columbia", "pct_free/reduced"] = districts.loc[districts.state=="District Of Columbia", "pct_free/reduced"].fillna("[0.6, 0.8[")
# districts.loc[districts.state=="Arizona", "pct_free/reduced"] = districts.loc[districts.state=="Arizona", "pct_free/reduced"].fillna("[0.4, 0.6[")
# districts.loc[districts.state=="Tennessee", "pct_free/reduced"] = districts.loc[districts.state=="Tennessee", "pct_free/reduced"].fillna("[0.4, 0.6[")
# districts.loc[districts.state=="Ohio", "pct_free/reduced"] = districts.loc[districts.state=="Ohio", "pct_free/reduced"].fillna("[0.4, 0.6[")


# # # imputing missing values in State column
# districts.loc[districts.state=="Connecticut", "pp_total_raw"] = districts.loc[districts.state=="Connecticut", "pp_total_raw"].fillna("[20000, 22000[")
# districts.loc[districts.state=="California", "pp_total_raw"] = districts.loc[districts.state=="California", "pp_total_raw"].fillna("[12000, 14000[")
# districts.loc[districts.state=="Ohio", "pp_total_raw"] = districts.loc[districts.state=="Ohio", "pp_total_raw"].fillna("[12000, 14000[")
# districts.loc[districts.state=="New Hampshire", "pp_total_raw"] = districts.loc[districts.state=="New Hampshire", "pp_total_raw"].fillna("[16000, 18000[")
# districts.loc[districts.state=="New York", "pp_total_raw"] = districts.loc[districts.state=="New York", "pp_total_raw"].fillna("[24000, 26000[")
# districts.loc[districts.state=="North Dakota", "pp_total_raw"] = districts.loc[districts.state=="North Dakota", "pp_total_raw"].fillna("[12000, 14000[")
# districts.loc[districts.state=="Arizona", "pp_total_raw"] = districts.loc[districts.state=="Arizona", "pp_total_raw"].fillna("[8000, 10000[")


# # # Creating the averages for all ranges columns
# districts['avg_black_hispanic'] = districts['pct_black/hispanic'].apply(avg_ranges)
# districts['avg_reduced_lunch'] = districts['pct_free/reduced'].apply(avg_ranges)
# districts['avg_spent_per_pupil'] = districts['pp_total_raw'].apply(avg_ranges)


# # # dropping the range columns
# districts.drop(["pct_black/hispanic",'pct_free/reduced'], axis=1, inplace=True)

# ##################
# # Products       #
# ##################

# products = pd.read_csv("./input/LearnPlatform/products_info.csv")
# # biufurcating the Primary Essential Column into Category and Sub_Category
# products["Category"] = products["Primary Essential Function"].apply(lambda x: str(x).split("-")[0])
# products["Sub_Category"] = products["Primary Essential Function"].apply(sub_category)

# # Segrregating the Sub-Categories
# products["Sub_Category"] = products["Sub_Category"].apply(lambda x: str(x).split("-")[0])

# # Replacing the string type nan values in Category and Sub-Category columns with np.nan 
# products[["Category","Sub_Category"]] = products[["Category","Sub_Category"]].replace("nan",np.nan)
# # Cleaning the Sub_Category
# products.Sub_Category = products.Sub_Category.replace([" Sites, Resources & Reference ",
#                                                                " Sites, Resources & Reference",
#                                                                " Sites, Resources & References "], 
#                                                                   "Sites, Resources & References")
# products.Sub_Category = products.Sub_Category.replace([" Data, Analytics & Reporting ",
#                                                                " Data, Analytics & Reporting"], 
#                                                                   "Data, Analytics & Reporting")
# products.Sub_Category = products.Sub_Category.replace([" Study Tools "," Study Tools"], 
#                                                                   "Study Tools")



# def goodFig():
#     # path = r"./input/engagement_data"
#     # filenames = glob.glob(path+"/*.csv")

#     # engagement = pd.DataFrame()
#     # for file in filenames:
#     #     b = pd.read_csv(file)
#     #     b["district_id"] = int(file.split("/")[-1].split(".")[0])
#     #     engagement = pd.concat([engagement,b])
#     #     print(len(engagement))
    
#     # engagement.to_csv('output/engagement.csv')
#     engagement = pd.read_csv('output/csv/engagement.csv')

#     print(engagement.shape)

#     engagement.reset_index(drop=True)
#     engagement.time = pd.to_datetime(engagement.time)
#     engagement.engagement_index.fillna(0, inplace=True)
#     engagement.pct_access.fillna(0, inplace=True)

#     # temp dataframe for computing enagement index and pct_access across all USA.
#     temp = engagement.groupby("time")[["engagement_index","pct_access"]].mean().reset_index()

#     # Plot showing overall enegamenet index and pct _access
#     fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, 
#                         subplot_titles=["<b>% At least 1 page Load Event <br> ", "<b>Page Loads per 1000 Students <br> "])

    

#     fig.add_trace(go.Scatter(x=temp.time, y=temp.pct_access, line=dict(color='#6C89AB')), row=1, col=1)
#     fig.add_trace(go.Scatter(x=temp.time, y=temp.engagement_index, line=dict(color='#904B53')), row=2, col=1)
#     fig.add_vrect(x0="2020-05-20", x1="2020-08-30", fillcolor="#9FC1D1", opacity=0.2, line_width=0)
#     fig.add_vrect(x0="2020-03-19", x1="2020-04-07", fillcolor="#EEDEB4", opacity=0.5, line_width=0)
#     # fig.add_vline(x="2020-01-21", line_dash="dot")
#     fig.add_vline(x="2020-02-03", line_dash="dot")
#     fig.add_vline(x="2020-07-16", line_dash="dot")


#     # fig.add_annotation(x="2020-01-21", y=150, text="First Case in USA", 
#     #                    ax=-40, ay=-50, row=2, col=1, arrowsize=2, arrowhead=2)
#     fig.add_annotation(x="2020-06-25", y=0.6, text="Summer Vacation", row=1, col=1, showarrow=False, font_color="#122139", font_size = 15)
#     fig.add_annotation(x="2020-06-25", y=180, text="Summer Vacation", row=2, col=1, showarrow=False, font_color="#122139", font_size = 15)
#     fig.add_annotation(x="2020-03-30", y=300, row=2, col=1, showarrow=False, font_color="#A47561",text="Lockdowns Start <br>in USA")
#     fig.add_annotation(x="2020-02-03", y=0.8, text="Public Health Emergency <br>Declared in USA<br> dated 2020-02-03", 
#                        ax=80, ay=-40, row=1, col=1, arrowsize=2, arrowhead=2)
#     fig.add_annotation(x="2020-07-16", y=0.8, text="New Record of Daily Cases - 76,000<br>in USA dated 2020-07-16", 
#                        ax=130, ay=-30, row=1, col=1, arrowsize=2, arrowhead=2)

#     fig.update_layout( showlegend=False, margin=dict(l=0, r=0, t=50), height=700)
#     fig.show()




# def dayOfWeek_Barplot():
#     engagement = pd.read_csv('output/csv/engagement.csv')
#     # extracting week of the year from time
#     engagement["week"] = pd.to_datetime(engagement.time).dt.weekofyear

#     # extracting day of week from time
#     engagement["day_of_week"] = pd.to_datetime(engagement.time).dt.dayofweek
#     # analysing the affect of day of the week on engagement_index and pct_access 
#     temp = engagement.groupby("day_of_week")[["engagement_index","pct_access"]].mean().reset_index()

#     # visulaizing the affect of day of the week on engagement_index and pct_access 
#     fig = bar_plot_day2week(temp, ["day_of_week"], ["engagement_index","pct_access"])
#     print(type(fig))
#     fig.update_layout(title=dict(text="<b>Day of the WEEK affect</b>", x=0.5, font_size=20))
#     fig.show()


# def compareEngagement():
#     # engagement = pd.read_csv('output/engagement.csv')
    
#     # # extracting week of the year from time
#     # engagement["week"] = pd.to_datetime(engagement.time).dt.weekofyear

#     # # extracting day of week from time
#     # engagement["day_of_week"] = pd.to_datetime(engagement.time).dt.dayofweek

#     # # Combining all the Dataframes
#     # df = pd.merge(engagement,districts, on="district_id", how="inner")
#     # df = pd.merge(df,products, left_on="lp_id", right_on="LP ID", how="inner")
#     # temp = df.groupby(["locale","week"])[["pct_access","engagement_index"]].mean().reset_index()
#     # temp.to_csv('output/localewise.csv')
#     districts.to_csv('input/newLearnPlatform/new_districts.csv', index = False)
#     products.to_csv('input/newLearnPlatform/new_products.csv', index = False)
#     temp = pd.read_csv('output/csv/localewise.csv')
#     # timePlot(temp, 'pct_access', 2)
#     # timePlot(temp, 'engagement_index', 550)
#     # time_plot_mine(temp)
#     # time_plot(temp, "locale","All")

# # goodFig()
# # dayOfWeek_Barplot()

# compareEngagement()

from plot import *
temp = pd.read_csv('output/csv/pp_engage_4.csv')
timePlot(temp, 'engagement_index', 4500)
