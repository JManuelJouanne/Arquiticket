from pydantic import BaseModel


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
