from sqlalchemy import * #specifically create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

#instantiate file
Base = declarative_base()


class Coach(Base):
    __tablename__ = 'coach'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    years = Column(Integer)
    salary = Column(Float)
    sal_school = Column(String)
    schools = relationship('School', secondary = 'joinedtable', back_populates = 'coaches')

class School(Base):
    __tablename__ = 'school'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    years = Column(String)
    winloss = Column(Float)
    team_points = Column(Float)
    opp_points= Column(Float)
    coaches = relationship('Coach', secondary = 'joinedtable', back_populates = 'schools')

class JoinedTable(Base): #create this table for a many to many relationship
    __tablename__ = 'joinedtable'
    school_id = Column(Integer, ForeignKey('school.id'), primary_key =True)
    coach_id = Column(Integer, ForeignKey('coach.id'), primary_key = True)

engine = create_engine('sqlite:///basketball.db')
Base.metadata.create_all(engine)
