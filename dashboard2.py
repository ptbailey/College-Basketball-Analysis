import dash
import dash_core_components as dcc
import dash_html_components as html
from __init__ import app2
from queries import *
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import math


trace = go.Scatter(
                x = [c[-1] for c in correlation()],
                y = [c[-2] for c in correlation()],
                mode = 'markers')

app2.layout = html.Div([
            dcc.Graph(
                id='correlation-graph',
                figure = {
                'data' : [
                    go.Scatter(
                    x = [c[2] for c in correlation()],
                    y = [c[-2] for c in correlation()],
                    mode = 'markers')],
                'layout' :
                    go.Layout(
                    xaxis = {"title" : "WinLoss %"},
                    yaxis = {"title" : "Salary of Coach"},
                    title = '"WinLoss % v. Coach Salary for 2011-2019'),

                })])

    # dcc.Graph(
    #   id='example-graph',
    #   figure={
    #       'data': [{'x': highest_salaries_info()[0], 'y': highest_salaries_info()[1], 'type': 'bar'}],
    #
    #       'layout': {'title': 'Win/Loss of Highest Paid Coaches by University'}
    #
    #           }
