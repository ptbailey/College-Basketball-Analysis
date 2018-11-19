from sqlalchemy.orm import sessionmaker
from models import *
#from seed import team_instances, coach_instances
from sqlalchemy import func
import math

Session = sessionmaker(bind = engine)
session = Session()

def average_all_coaches_salary():
    x = session.query(func.AVG(Coach.salary)).filter(Coach.salary!=0).all()
    return round(x[0][0],2)

def average_coach_salary():
    return session.query(Coach.name, func.AVG(Coach.salary), Coach.sal_school, Coach.years).group_by(Coach.name).all()

def point_differentials():
    return session.query(School.name,School.years,School.team_points-School.opp_points).all()

def team_with_best_pd():
    pd = point_differentials()
    maxx = max([i[2] for i in pd])
    x = [p[0] for p in pd if p[2] == maxx]
    return x, maxx

def team_with_worst_pd():
    pd = point_differentials()
    minn = min([i[2] for i in pd])
    x = [p[0] for p in pd if p[2] == minn]
    return x, minn

def top_5_highest_average_salary():
    return session.query(Coach.name,func.AVG(Coach.salary)).group_by(Coach.name).order_by(func.AVG(Coach.salary).desc()).limit(5).all()

#match the names in highest_average_salary() with name in School.coaches and print out the winloss
def highest_avg_salaries_info():
    wanted_data = session.query(School.name,School.winloss,Coach.name,Coach.salary, Coach.years).join(JoinedTable).join(Coach).all()
    filtered = []
    for tup in wanted_data:
        for h_tup in top_5_highest_average_salary():
            if tup[2] == h_tup[0]:
                filtered.append(tup)
    return filtered

def correlation():
    return session.query(School.name,School.years,School.winloss,Coach.name,\
    Coach.salary,Coach.years).join(JoinedTable).join(Coach).all()
