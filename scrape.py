import requests
from bs4 import BeautifulSoup # Python package for parsing HTML and XML documents.
                              # It creates a parse tree for parsed pages that
                              # can be used to extract data from HTML, which is
                              #useful for web scraping
import re #requests.get gets the url information
import json #loads json APIs

class TeamSite:
    def __init__(self, college,year1,year2):
        self.name = college
        self.year1 = year1
        self.year2 = year2
        r = requests.get('https://www.sports-reference.com/cbb/schools/{college}/'.format(college = college))
        c = r.content #to see the content of the URL site
        self.soup = BeautifulSoup(c, 'html.parser') # bs4 parses the html data
        self.index = (self.year2-self.year1)

    @property
    def years(self):
        college = self.name
        years = []
        no_data = []
        for i in range(self.year1+1,self.year2+1):
            x = self.soup.findAll('a', {'href':'/cbb/schools/{name}/{year}.html'.format(name = college, year = i)})
            if len(x) == 0:
                no_data.append(x)
            else:
                y = ((self.soup.findAll('a', {'href':'/cbb/schools/{name}/{year}.html'.format(name = college, year = i)}))[0]).text
                years.append(y)
                years.sort()
                years.reverse()
        return years #had to reverse the list because the way winloss is reading
                                # is from top year (2019) to lowest year, but this years function
                                # is reading it with index(lowest year to highest year)

    @property
    def winloss(self):
        whole = self.soup.findAll('td', {'class' : "right", 'data-stat' : 'win_loss_pct'})
        almost = [i.text for i in whole]
        return almost[:self.index]

    @property
    def team_points(self):
        whole = self.soup.findAll('td', {'class': 'right', 'data-stat': 'pts_per_g'})
        almost = [i.text for i in whole]
        return almost[:self.index]

    @property
    def opp_points(self):
        whole = self.soup.findAll('td', {'class': 'right', 'data-stat': 'opp_pts_per_g'})
        almost = [i.text for i in whole]
        return almost[:self.index]

    @property
    def coaches_names(self):
        whole = self.soup.findAll('td', {'class': 'left', 'data-stat': 'coaches'})
        almost = [i.text for i in whole]
        coaches = almost[:self.index]
        listy = []
        for coach in coaches:
            first = coach.rindex('(')
            space = coach[first-1:]
            clean = (coach.replace(space,''))
            listy.append(clean)
        return listy

class CoachSite:
    def __init__(self):
        r = requests.get('http://sports.usatoday.com/ncaa/salaries/mens-basketball/coach/#')
        c = r.content
        self.soup = BeautifulSoup(c, 'html.parser')

    @property
    def tags(self):
        coaches_ids = []
        not_coaches_ids = []
        for tag in self.soup.findAll('td',{"class": ''}):
            try:
                coaches_ids.append((tag['data-coach']))
            except KeyError:
                not_coaches_ids.append(0)
        return coaches_ids

    @property
    def pages(self):
        coaches_pages = []
        for id in self.tags:
            r = requests.get('''http://sports.usatoday.com/ajaxservice/ncaa/salaries__coach__'''+id)
            c = r.content
            data = json.loads(c)
            coaches_pages.append(data)
        return coaches_pages

    @property
    def salaries(self):
        coaches_pages = self.pages
        necess_info = list(map(lambda coach : coach['rows'],coaches_pages))
        listy = []
        schools = []
        coach_name = list(map(lambda coach: coach['profile']['coach_name'],coaches_pages))
        for i in range(0,len(necess_info)):
            for ii in range(0,len(necess_info[i])):
                year = necess_info[i][ii]['year']['value']
                salary = necess_info[i][ii]['total_pay']['value']
                school = necess_info[i][ii]['school_name']['value']
                schools.append(school)
                tup = (coach_name[i], year,salary,school)
                listy.append(tup)
        return listy, list(set(schools))
