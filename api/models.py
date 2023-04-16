from sqlalchemy import Column, Integer, String

from .database import Base


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    location = Column(String)
    latitude = Column(Integer)
    longitude = Column(Integer)
