#!/usr/bin/python3
"""data base storage engine"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


class DBStorage:
    """dbstorage engine class"""
    __engine = None
    __session = None

    def __init__(self):
        user = os.getenv("HBNB_MYSQL_USER")
        passwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        mode = os.getenv("HBNB_ENV")
        db_url = f"mysql+mysqldb://{user}:{passwd}@{host}/{db}"
        self.__engine = create_engine(db_url, pool_pre_ping=True)
        if mode == "test":
            tables = ["users", "places", "states", "cities",
                      "amenities", "reviews"]
            pre_drop = "SET FOREIGN_KEY_CHECKS=0;"
            post_drop = "SET FOREIGN_KEY_CHECKS=1;"
            with self.__engine.connect() as conn:
                for table in tables:
                    txt = f"{pre_drop}drop table if exists {table};\
                            {post_drop}"
                    conn.execute(text(txt))

    def all(self, cls=None):
        """returns all objs of type cls"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        cls_dict = {"BaseModel": BaseModel, "User": User,
                    "Place": Place, "State": State, "City": City,
                    "Amenity": Amenity, "Review": Review}
        dct = {}
        if cls:
            list_of_obj = self.__session.query(cls).all()
            for obj in list_of_obj:
                dct[f"{cls.__name__}.{obj.id}"] = obj
            return dct

        for cls_ in cls_dict.values():
            list_of_obj = []
            try:
                list_of_obj = self.__session.query(cls_).all()
            except Exception:
                pass
            for obj in list_of_obj:
                dct[f"{cls_.__name__}.{obj.id}"] = obj
        return dct

    def new(self, obj):
        """adds obj to the current session"""
        self.__session.add(obj)

    def save(self):
        """commits current transaction"""
        self.__session.commit()

    def delete(self, obj=None):
        """remove obj from the current session"""
        self.__session.delete(obj)

    def reload(self):
        """create all tables in the database """
        from models.base_model import Base
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        from sqlalchemy.orm import scoped_session
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
