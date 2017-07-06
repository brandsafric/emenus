import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    address = Column(String(250), nullable = False)
    city = Column(String(50), nullable = False)
    state = Column(String(20), nullable = False)
    zipCode = Column(String(20), nullable = False)
    website = Column(String(250), nullable = True)
    id = Column(Integer, primary_key = True)


class Puppy(Base):

    __tablename__ = 'puppy'

    name = Column(String(80), nullable = False)
    date_of_birth = Column(String(100), nullable = False)
    gender = Column(String(20), nullable = False)
    weight = Column(String(50), nullable = False)
    shelter_id = Column(Integer, ForeignKey('shelter.id'), primary_key = True)
    picture = Column(String(250), nullable = True)
    shelter = relationship(Shelter)

engine = create_engine('sqlite:///puppies.db')
Base.metadata.create_all(engine)

