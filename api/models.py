from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base



"""
{
   "name": string,
   "date": string (ISO 8601 https://es.wikipedia.org/wiki/ISO_8601),
   "price": number,
   "quantity": number,
   "location": string,
   "latitude": number,
   "longitude" number
},

{
   "name": "EXPO LONCOCHE 2023  JUEVES 23",
   "date": "2023-01-17T00:00:00",
   "price": 2000,
   "quantity": 10000,
   "location": "PARCELA MUNICIPAL",
   "latitude": -33.455275555427804,
   "longitude": -70.6605295633026
},



"""
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

