from pydantic import BaseModel


class EventBase(BaseModel):
    event_id: str
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
    event_id: str

    class Config:
        orm_mode = True


class RequestBase(BaseModel):
    request_id: str
    group_id: str
    event_id: str
    deposit_token: str
    quantity: int
    seller: int


class RequestCreate(RequestBase):
    pass


class Request(RequestBase):
    request_id: str

    class Config:
        orm_mode = True


class TicketBase(BaseModel):
    request_id: str
    user_id: str
    event_id: str
    quantity: int
    status: int


class TicketCreate(TicketBase):
    pass


class Ticket(TicketBase):
    request_id: str

    class Config:
        orm_mode = True
