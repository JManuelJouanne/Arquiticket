from sqlalchemy.orm import Session

from db import schemas
from . import models


def get_event(db: Session, event_id: str):
    return db.query(models.Event).filter(models.Event.event_id == event_id).first()


def update_event(db: Session, event_id: str, discount: int):
    db.query(models.Event).filter(models.Event.event_id == event_id).first().quantity -= discount
    db.commit()


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_request(db: Session, request_id: str):
    return db.query(models.Request).filter(models.Request.request_id == request_id).first()


def get_requests_user(db: Session, user_id: str):
    return db.query(models.Request).filter(models.Request.user_id == user_id).all()


def create_request(db: Session, event: schemas.RequestCreate):
    db_request = models.Request(**event.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def get_ticket(db: Session, request_id: str):
    return db.query(models.Ticket).filter(models.Ticket.request_id == request_id).first()


def get_tickets_user(db: Session, user_id: str, status: int):
    return db.query(models.Ticket).filter(models.Ticket.user_id == user_id,
                                          models.Ticket.status == status).all()


def create_ticket(db: Session, ticket: schemas.TicketCreate):
    db_ticket = models.Ticket(**ticket.dict())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def update_ticket(db: Session, request_id: str, status: int):
    db.query(models.Ticket).filter(models.Ticket.request_id == request_id).first().status = status
    db.commit()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_money(db: Session, user_id: str):
    print(" d")
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def add_money(db: Session, user_id: str, quantity: int):
    db.query(models.User).filter(models.User.user_id == user_id).first().money += quantity
    db.commit()


def use_money(db: Session, user_id: str, quantity: int):
    db.query(models.User).filter(models.User.user_id == user_id).first().money -= quantity
    db.commit()
