import dash
import dash_core_components as dcc
import dash_html_components as html
from __init__ import app
from queries import *
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import math


########### For Tab 1 ##############
school_names = list(set([tup[0] for tup in point_differentials()]))
d = {}
for tup in point_differentials():
    d.setdefault(tup[0],[])
    d[tup[0]].append((tup[1],tup[2]))

########### For Tab 2 ##############
coach_names = [tup[0] for tup in average_coach_salary()]
coach_salaries = [tup[1] for tup in average_coach_salary()]

y = len(coach_names)*[average_all_coaches_salary()]
avg_sal = go.Scatter(x = coach_names, y = y, name = 'Average of all Coaches\' Salaries')
############ Build two Tabs ####################################################
app.layout = html.Div([
    dcc.Tabs(id="tabs", children=[

    ################## Tab 1: dropdown for schools and pt. diff ################
        dcc.Tab(id='Tab 1', label='Point Differential', children=[
            html.H2(children='Pick schools to compare their point differential over time'),
            dcc.Dropdown(
                id = 'my-dropdown',
                options = [{'label':school_name.title(), 'value': school_name } for school_name in school_names],
                value = "syracuse"),
            dcc.Graph(
                id='ptdiff-graph'),
            dcc.Dropdown(
                id = 'second-dropdown',
                options = [{'label':school_name.title(), 'value': school_name } for school_name in school_names],
                value = "boston-university"),
            dcc.Graph(
                id = 'other-ptdiff-graph')
            ]),

    ################## Tab 2: coach salary #####################################
        dcc.Tab(id='Tab 2', label='Coaches Salary', children=[
            html.H2(children='Coaches Salary'),
            dcc.Graph(
                id='salary-graph',
                figure={
                    'data': [
                        {'x': coach_names, 'y': coach_salaries, 'type': 'bar',
                        'name' : "Average Salary for each Coach"},
                        avg_sal],
                    'layout': {'title': 'Average Salaries per Coach from 2011 - 2018'}})])])])

@app.callback(
dash.dependencies.Output('ptdiff-graph', 'figure'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_graph(value):
    figure = {'data': [
        {'x': [(index[0][0:5] + "  " + index[0][5:]) for index in d[value]],
        'y' : [index[1] for index in d[value]]
        }]}
    return figure

@app.callback(
dash.dependencies.Output('other-ptdiff-graph', 'figure'),
    [dash.dependencies.Input('second-dropdown', 'value')])
def update_graph(value):
    figure = {'data': [
        {'x': [(index[0][0:5] + "  " + index[0][5:]) for index in d[value]],
        'y' : [index[1] for index in d[value]]
        }]}
    return figure
