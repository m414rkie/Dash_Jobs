# A code to visualize and track my job search.

# Jon Parsons
# 12-15-2020

# -*- coding: utf-8 -*-


import json
import os
import dash
import numpy as np
import pandas as pd
import plotly.express as px
import dash_table as td
import dash_core_components as dcc
import dash_html_components as html

from datetime import date
from datetime import datetime
from Subroutines import job_search_subs as sbs
from Subroutines import job_search_web_subs as web
from dash.dependencies import Input, Output, State
today = datetime.now()
today_str = today.strftime('%d/%m/%y')

data_file = 'data/applications.json'

ext_style =  ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df_jobs = sbs.load_data(data_file)

page = dash.Dash(__name__, external_stylesheets=ext_style)

def serve_layout():

    return html.Div(

        children=[
        # Headers
        html.H1(children="Job Search by the Numbers",
            style={
            'textAlign':'center'
            }
        ),
        # Refresh button to update data
        html.A(html.Button('Refresh Page'), href='/'),
        # current plot
        html.H3(children='''Plot''',
            style={'textAlign':'center'
            }
        ),
        # show plot here
        html.Div([
            dcc.Graph(
                id='bar_job',
                figure={}
            ),
            # refresh interval here
            dcc.Interval(
                id='graph_int',
                interval=2500,
                n_intervals=0
            )
        ]),

        html.Div(
            id='average'
        ),
        # get information for a new job entry
        html.Div(
            children=[
                html.Div(children='''Did you apply to a new job? Enter the data here'''),
                dcc.Input(id='Company', value='Company', type='text'),
                html.Br(),
                dcc.Input(id='Applied', value='dd/mm/yyyy', type='text'),
                html.Br(),
                dcc.Input(id='Type', value='Type', type='text'),
                html.Br(),
                dcc.Input(id='Location', value='Location', type='text'),
                html.Br(),
                html.Button('Submit',id='new_job_submit', n_clicks=0, type='submit',
                    style={'backgroundColor': 'salmon'}),
                html.Br(),
                html.Div(id='new_job_info')
            ]
        ),
        # displays table of information
        html.Div(children='''Data Table''',
            style={'textAlign':'center'
            }
        ),
        td.DataTable(
            id='table',
            columns = [{'name':i, 'id':i} for i in df_jobs.columns],
            data = df_jobs.to_dict('records')
        ),

    ])

################################################################################
############################# Page Callbacks ###################################
################################################################################

### Determines graph on page
@page.callback(
    Output('bar_job', 'figure'),
    Input('graph_int','n_intervals')
    )
def update_graph(Graph):
# for now just a horizontal bar chart with number days since application
    df = pd.read_json(data_file,orient='index')
    graph = sbs.days_since(df)
    return graph

### New job input
@page.callback(
    Output('new_job_info', 'children'),
    [Input('new_job_submit', 'n_clicks')],
    state=[
        State('Company', 'value'),
        State('Applied', 'value'),
        State('Type', 'value'),
        State('Location', 'value')
    ]
)
def new_job(n_clicks,Company,Applied,Type,Location):
    df = pd.read_json(data_file,orient='index')

    if n_clicks > 0:
        new_job = sbs.insert_new_job(
                                df,Company,Applied,
                                Type,Location,data_file
                                )
        n_clicks = 0
        return "New Job Submitted!"
    else:
        return ""

################################################################################
########################## End Page Callbacks ##################################
################################################################################


page.layout = serve_layout()


if __name__ == '__main__':
    page.run_server(debug=True)
