from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import requests
# from dash_package import db
# from dash_package.flask_models import *
# from dash_package.scrape import *
from scrape import *
from models import Coach, School

engine = create_engine('sqlite:///basketball.db')
Session = sessionmaker(bind = engine)
session = Session()

def Instantiate(year1,year2):
    coachsite_objects = CoachSite()
    lowered = list(map(lambda school : school.lower(),coachsite_objects.salaries[1]))
    school_list = list(map(lambda school : school.replace(' ', '-'), lowered))
    teamsite_objects = {}
    for school in school_list:
        teamsite_objects[school] = TeamSite(school,year1,year2)
    return teamsite_objects, coachsite_objects

everything = (Instantiate(2011,2019))
teamsite = everything[0] # gives you a dictionary with keys = school name and values\n",
             # are TeamSite instances\n",
keys = list((teamsite).keys())
coachsite = everything[1] #gives you object instance\n",

#######Instansiate coach model##########
coach_instances = []
for tup in coachsite.salaries[0]:
    tup2 = int(tup[2].replace('$','').replace(',',''))
    c_instance = Coach(name = tup[0] , years = tup[1] , salary = tup2,\
                       sal_school = tup[3])
    coach_instances.append(c_instance)
    session.add(c_instance)

#######Instansiate school model##########
team_instances = []
for school_name in keys:
    years_ = teamsite[school_name].years
    winloss_ = teamsite[school_name].winloss
    team_points_ = teamsite[school_name].team_points
    opp_points_ = teamsite[school_name].opp_points

    for i in range(0,len(years_)):
        if years_[i] != '' and winloss_[i] != '' and team_points_[i] != '' and opp_points_[i] != '':
            team_instance = School(name = school_name, years = years_[i], winloss = winloss_[i],\
                            team_points = team_points_[i], opp_points = opp_points_[i])
            for coach in coach_instances:
                if coach.sal_school.replace(' ', '-').lower() == team_instance.name and coach.years == (team_instance.years)[:-3]:
                    team_instance.coaches.append(coach)
                    team_instances.append(team_instance)
                    session.add(team_instance)
                else:
                    session.add(team_instance)

session.commit()
