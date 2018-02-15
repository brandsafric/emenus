import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    path = Column(String(250))
    picture = Column(String(250))

class Picture(Base):
    __tablename__ = 'picture'
    id = Column(Integer, primary_key=True)
    filename = Column(String(250), nullable=False)
    path = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializable format
        return {
            'filename': self.filename,
            'id': self.id,
            'path': self.path
        }

class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    cuisine = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    picture_path = Column(String(250), ForeignKey('picture.path'))
    picture_id = Column(Integer, ForeignKey('picture.id'))
    picture = relationship(Picture)
    @property
    def serialize(self):
        # Returns object data in easily serializable format
        return {
            'name': self.name,
            'id' : self.id,
            'cuisine': self.cuisine,
            'picture': self.picture,
            'picture_path': self.picture_path
        }

class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializable format
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course
        }

# engine = create_engine('sqlite:///restaurantmenuwithusers.db')
engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.create_all(engine)