from config import SQLALCHEMY_DATABASE_URL
from config import SQLALCHEMY_MIGRATE_REPO
import os,sys

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Boolean
from sqlalchemy.orm import relationship,backref

Base = declarative_base()

association_table = Table('association',Base.metadata,
    Column('route_id', Integer, ForeignKey('routes.id')),
    Column('competitor_id', Integer, ForeignKey('competitor.id'))
)

class Competitor(Base):
    __tablename__ = 'competitor'
    
    # Here we define columns for the table person
    id      = Column(Integer, primary_key=True)
    name    = Column(String(250), nullable=False, unique=True)
    team    = Column(String(250), nullable=False)
    male    = Column(Boolean, nullable=False)

    routes_id   = Column(Integer, ForeignKey('routes.id'))
    routes      = relationship('Routes', secondary=association_table) #,uselist=True)  #, backref=backref('competitor',lazy='dynamic'))
    
class Routes(Base):
    __tablename__ = 'routes'
    # Here we define columns for the table person
    id              = Column(Integer, primary_key=True)
    
    #Route Specific Parameters
    name            = Column(String(250), nullable=False)
    grade           = Column(String(250), nullable=False)
    points          = Column(Integer, nullable=False)
    lead_only       = Column(Boolean, nullable=False)
    
    competitor_id   = Column(Integer, ForeignKey('competitor.id'))
    #competitor      = relationship('Competitor',back_populates='routes')
    
class Score(Base):
    __tablename__ = 'score'
    id              = Column(Integer, primary_key=True)
    grade           = Column(String(250), nullable=False, unique=True)
    points          = Column(Integer, nullable=False)
    type            = Column(String(250), nullable=False)
    
    

################################################################################
##              Functions for interfacing with the database
################################################################################
def Create_db():
    """Create the initial database"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(engine)
    
def Competitor_Insert(name,team,male):
    """Insert a new competitor into the database.
        @param name  (string)   : Name of Competitor
    """
    new_competitor = Competitor(name=name,team=team,male=male)
    session.add(new_competitor)
    try :
        session.commit()
    except : pass
    
def Get_Competitors():
    """Get a list of all players in the competition
        @return (list) : List of all Competitors
    """
    # Make a query to find all Persons in the database
    comps = session.query(Competitor).all()
    return comps

def Get_Competitor(name):   
    """Get a specific player in the competition
        @return (Competitor) : Specific competitor
    """
    return session.query(Competitor).filter(Competitor.name == name).one()

def Get_Session():
    """Get a session of the database
        @return (DBSession) : Data base session    
    """
    engine              = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.bind  = engine
    DBSession           = sessionmaker()
    DBSession.bind      = engine
    session             = DBSession()
    return session

def Set_Point_Values(routes,boulders):
    """Takes a dictionary of routes and a dictionary of boulder with
        corresponding point values."""
    for key,value in routes.iteritems() : 
        print '1',key
        session.add(Score(grade=key,points=value,type='route'))
    for key,value in boulders.iteritems() : 
        print '2',key
        session.add(Score(grade=key,points=value,type='boulder'))
    session.commit()

    
session = Get_Session()    
 
#Purely test data
b_points = {'VB':10,'V0':17}
r_points = {'5.5':2,'5.9':10}

"""
Create_db()
Competitor_Insert("Johnny","1",False)
Competitor_Insert("Michael","2",True)
Set_Point_Values(r_points,b_points)
for i in Get_Competitors(): print i.name
print Get_Competitor("Johnny").male


r1 = Routes(grade='5.8',points=1230,lead_only=True, name='blablah')
r2 = Routes(grade='5.9',points=12,lead_only=False, name='nasdf')
session.add(r1)
session.add(r2)
session.commit()
"""
j = Get_Competitor("Johnny")
#j.routes.append(r2)

m = Get_Competitor("Michael")
#m.routes.append(r2)
#m.routes.append(r1)
#session.commit()

for r in j.routes : print 'j : ',r.name
for r in m.routes : print 'm : ',r.name
