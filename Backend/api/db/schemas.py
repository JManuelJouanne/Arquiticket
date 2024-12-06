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
    assigned: int = 0


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
    link: str


class TicketCreate(TicketBase):
    pass


class Ticket(TicketBase):
    request_id: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    user_id: str
    money: int
    admin: bool = False


class UserCreate(UserBase):
    pass


class User(UserBase):
    user_id: str

    class Config:
        orm_mode = True


class OfferBase(BaseModel):
    auction_id: str
    proposal_id: str
    event_id: str
    quantity: int
    group_id: int
    type: str
    status: int = 2


class OfferCreate(OfferBase):
    pass


class Offer(OfferBase):
    auction_id: str

    class Config:
        orm_mode = True


class ProposalBase(BaseModel):
    auction_id: str
    proposal_id: str
    event_id: str
    quantity: int
    group_id: int
    type: str
    status: int = 2


class ProposalCreate(ProposalBase):
    pass


class Proposal(ProposalBase):
    proposal_id: str

    class Config:
        orm_mode = True


class AcceptanceBase(BaseModel):
    auction_id: str
    proposal_id: str
    event_id: str
    quantity: int
    group_id: int
    type: str
    status: int = 2


class AcceptanceCreate(AcceptanceBase):
    pass


class Acceptance(AcceptanceBase):
    proposal_id: str

    class Config:
        orm_mode = True
