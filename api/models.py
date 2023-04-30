from sqlalchemy import Column, Integer, String

from .database import Base


class Event(Base):
    __tablename__ = "events"
    event_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    date = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    location = Column(String)
    latitude = Column(Integer)
    longitude = Column(Integer)


class Request(Base):
    __tablename__ = "requests"
    request_id = Column(String, primary_key=True, index=True)
    group_id = Column(String)
    event_id = Column(String)
    deposit_token = Column(String)
    quantity = Column(Integer)
    seller = Column(Integer)


class Ticket(Base):
    __tablename__ = "tickets"
    request_id = Column(String, primary_key=True, index=True)
    user_id = Column(String)
    event_id = Column(String)
    quantity = Column(Integer)
    status = Column(Integer)
