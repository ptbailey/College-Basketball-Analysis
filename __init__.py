from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dash

server = Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///basketball.db'
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
server.config["SQLALCHEMY_ECHO"] = True

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/', external_stylesheets=external_stylesheets)
app1 = dash.Dash(__name__, server=server, url_base_pathname='/dashboard1/', external_stylesheets=external_stylesheets)
app2 = dash.Dash(__name__, server=server, url_base_pathname='/dashboard2/', external_stylesheets=external_stylesheets)

from dashboard import *
from dashboard1 import *
from dashboard2 import *
from queries import *
