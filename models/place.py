#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Integer, Column, String,\
    ForeignKey, Float
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"),
                     nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"),
                     nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0,
                          nullable=False)
    number_bathrooms = Column(Integer, default=0,
                              nullable=False)
    max_guest = Column(Integer, default=0,
                       nullable=False)
    price_by_night = Column(Integer, default=0,
                            nullable=False)
    latitude = Column(Float())
    longitude = Column(Float())
    user = relationship("User", back_populates="places")
    cities = relationship("City", back_populates="places")
    reviews = relationship('Review', back_populates='place',
                           cascade='all, delete, delete-orphan')

    def get_reviews(self):
        """returns a list of all reviews with place_id
        equal to self.id"""
        from models import storage
        from models.review import Review
        lst = []

        for obj in storage.all(Review).values():
            if obj.place_id == self.id:
                lst.append(obj)

        return lst
