from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from sqlalchemy import func

from puppies import Base, Shelter, Puppy

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# 1. Query all of the puppies and return the results in ascending alphabetical order

puppies = session.query(Puppy.name).order_by('Puppy.name').all()

for puppy in puppies:
    print puppy.name


# 2. Query all of the puppies that are less than 6 months old organized by the youngest first
date_now = datetime.datetime.today()
six_months = datetime.timedelta(weeks = 24)
six_months_ago = date_now - six_months

young_puppies = session.query(Puppy.name, Puppy.dateOfBirth).filter(Puppy.dateOfBirth > six_months_ago).order_by('Puppy.dateOfBirth desc').all()

for puppy in young_puppies:
    print puppy.name
    print puppy.dateOfBirth

# 3. Query all puppies by ascending weight

puppies_weight = session.query(Puppy.name, Puppy.weight).order_by('Puppy.weight asc').all()

for puppy in puppies_weight:
    print puppy.name
    print puppy.weight

# 4. Query all puppies grouped by the shelter in which they are staying
puppies_shelter = session.query(Shelter, func.count(Puppy.shelter_id).label('Total')).join(Puppy.shelter).group_by(Puppy.shelter_id).order_by('Total asc').all()

# puppies_shelter = session.query(Puppy.name, Puppy.shelter_id).group_by(Puppy.shelter_id).all()

puppies_shelter = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()

for shelter in puppies_shelter:
    print shelter[0].id, shelter[0].name, shelter[1]

