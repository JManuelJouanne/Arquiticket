from sqlalchemy import Column, Integer, String, Boolean
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
    assigned = Column(Integer)


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
    link = Column(String)


class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True, index=True)
    money = Column(Integer)
    admin = Column(Boolean)


class Offer(Base):
    __tablename__ = "offers"
    auction_id = Column(String, primary_key=True, index=True)
    proposal_id = Column(String)
    event_id = Column(String)
    quantity = Column(Integer)
    group_id = Column(Integer)
    type = Column(String)
    status = Column(Integer)  # 0: rejected, 1: accepted, 2: pending


class Proposal(Base):
    __tablename__ = "proposals"
    auction_id = Column(String)
    proposal_id = Column(String, primary_key=True, index=True)
    event_id = Column(String)
    quantity = Column(Integer)
    group_id = Column(Integer)
    type = Column(String)
    status = Column(Integer)  # 0: rejected, 1: accepted, 2: pending
