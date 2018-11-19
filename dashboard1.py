import dash
import dash_core_components as dcc
import dash_html_components as html
from __init__ import app1
from queries import *
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import math

def avg_salaries():

    coach_names = [tup[0] for tup in average_coach_salary()]
    coach_salaries = [tup[1] for tup in average_coach_salary()]

    return [coach_names, coach_salaries]

def highest_salaries():

    coaches = [tup[0] for tup in top_5_highest_average_salary()]
    coaches_salaries = [tup[1] for tup in top_5_highest_average_salary()]

    return [coaches,coaches_salaries]

def highest_salaries_info():
    school = [tup[0].title() for tup in highest_avg_salaries_info()]

    winloss = [tup[1] for tup in highest_avg_salaries_info()]

    return [school,winloss]

app1.config.suppress_callback_exceptions = True

app1.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    html.H1('Patrina and Darshan\'s College Basketball Project'),

    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])

page_1_layout = html.Div([
    html.H1('Average Salary of the Highest Paid Coaches in College Basketball'),
    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),

    html.Div(children='''

  '''),

    dcc.Graph(
      id='example-graph',
      figure={
          'data': [{'x': highest_salaries()[0], 'y': highest_salaries()[1], 'type': 'bar'}],

          'layout': {'title': 'Top 5 Highest Paid Coaches'}

              }
  )


])

@app1.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)

page_2_layout = html.Div([
    html.H1('Win Loss Percentage of Schools of the 5 Highest Paid Coaches'),

    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
    html.Div(children='''

  '''),

    dcc.Graph(
      id='example-graph',
      figure={
          'data': [{'x': highest_salaries_info()[0], 'y': highest_salaries_info()[1], 'type': 'bar'}],

          'layout': {'title': 'Win/Loss of Highest Paid Coaches by University'}

              }
  )

])

@app1.callback(dash.dependencies.Output('page-2-content', 'children'),
              [dash.dependencies.Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


# Update the index
@app1.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page
