from pydantic import BaseModel

"""
-CREATE TABLE accounts (
user_id serial PRIMARY KEY,
	username VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR ( 50 ) NOT NULL,
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
	created_on TIMESTAMP NOT NULL,
last_login TIMESTAMP 
);
"""
# Hola

"""
Migrations:
CREATE TABLE event (
id serial PRIMARY KEY,
name VARCHAR(255),
date VARCHAR(255),
price INT,
quantity INT,
location VARCHAR(255),
latitude INT,
longitude INT,
);


"""


class EventBase(BaseModel):
    name: str
    date: str
    price: int
    quantity: int
    location: str
    latitude: int
    longitude: int


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int

    class Config:
        orm_mode = True
