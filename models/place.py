#!/usr/bin/python3
""" Place Module for HBNB project, new storage engine = SQLAlchemy"""
from models.base_model import BaseModel, Base
from sqlalchemy import Integer, Column, String,\
    ForeignKey, Float, Table
from sqlalchemy.orm import relationship


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', ForeignKey('places.id')),
                      Column('amenity_id', ForeignKey('amenities.id'))
                      )


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
    amenities = relationship('Amenity',
                             secondary='place_amenity',
                             back_populates='place_amenities')
    amenity_ids = []

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

    def get_amenities(self):
        """gets amenities associated with self"""
        from models import storage
        from models.Amenity import Amenity
        lst = []
        for obj in storage.all(Amenity).values():
            if obj.place_id == self.id:
                lst.append(obj)
        return lst

    def set_amenities(self, obj):
        """sets amenity associated with self"""
        if obj.__class__.__name__ == 'Amenity':
            self.amenity_ids.append(obj.id)
