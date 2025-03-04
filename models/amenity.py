#!/usr/bin/python3
""" State Module for HBNB project, new storage engine = SQLAlchemy"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """ amenities class"""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    place_amenities = relationship('Place',
                                   secondary='place_amenity',
                                   back_populates='amenities')
