import pandas as pd
import plotly.graph_objects as go

from plot import *
from plotly.subplots import make_subplots
def pageLoad2Week():
    engagement = pd.read_csv('input/csv/engagement.csv')
    engagement.reset_index(drop=True)
    engagement.time = pd.to_datetime(engagement.time)
    engagement.engagement_index.fillna(0, inplace=True)
    engagement.pct_access.fillna(0, inplace=True)

    # temp dataframe for computing enagement index and pct_access across all USA.
    temp = engagement.groupby("time")[["engagement_index","pct_access"]].mean().reset_index()

    # Plot showing overall enegamenet index and pct _access
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, 
                        subplot_titles=["<b>% At least 1 page Load Event <b> ", "<b>Page Loads per 1000 Students <b> "])
    fig.update_annotations(font=dict(size=30))

    fig.add_trace(go.Scatter(x=temp.time, y=temp.pct_access, line=dict(color='#6C89AB')), row=1, col=1)
    fig.update_layout(yaxis = dict(tickfont = dict(size=18)))
    fig.add_trace(go.Scatter(x=temp.time, y=temp.engagement_index, line=dict(color='#904B53')), row=2, col=1)
    fig.update_layout(yaxis2 = dict(tickfont = dict(size=18)))
    fig.update_layout(xaxis2 = dict(tickfont = dict(size=20)))
    fig.add_vrect(x0="2020-05-20", x1="2020-08-30", fillcolor="#9FC1D1", opacity=0.2, line_width=0)
    fig.add_vrect(x0="2020-03-19", x1="2020-04-07", fillcolor="#EEDEB4", opacity=0.5, line_width=0)
    # fig.add_vline(x="2020-01-21", line_dash="dot")
    fig.add_vline(x="2020-02-03", line_dash="dot")
    fig.add_vline(x="2020-07-16", line_dash="dot")


    fig.add_annotation(x="2020-06-25", y=0.6, text="Summer Vacation", row=1, col=1, showarrow=False, font_color="#122139", font_size = 20)
    fig.add_annotation(x="2020-06-25", y=180, text="Summer Vacation", row=2, col=1, showarrow=False, font_color="#122139", font_size = 20)
    fig.add_annotation(x="2020-03-30", y=300, row=2, col=1, showarrow=False, font_color="#A47561",text="Lockdowns Start <br>in USA", font_size = 20)
    fig.add_annotation(x="2020-02-03", y=0.8, text="Public Health Emergency <br>Declared in USA<br> dated 2020-02-03", ax=80, ay=-40, row=1, col=1, arrowsize=2, arrowhead=2)
    fig.add_annotation(x="2020-07-16", y=0.8, text="New Record of Daily Cases - 76,000<br>in USA dated 2020-07-16", ax=130, ay=-30, row=1, col=1, arrowsize=2, arrowhead=2)
    fig.update_layout( showlegend=False, margin=dict(l=0, r=0, t=50), height=1000)
    
    fig.show()
    fig.write_image('output/png/week2pageLoad.png',scale=0.9, width=2400, height=1000)
    fig.write_image('output/pdf/week2pageLoad.pdf',scale=0.9, width=2400, height=1000)

pageLoad2Week()

