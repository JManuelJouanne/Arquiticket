from fastapi import Request, APIRouter, Depends
from db.get import get_db
from db import crud, schemas
from mailing import send_notification
from requests.models import Response
from sqlalchemy.orm import Session
import uuid


events = APIRouter()


def generate_uuid():
    return str(uuid.uuid4())


@events.get("/events/user", response_model=list[schemas.Event])
def read_events_user(page: int = 1, count: int = 25, db: Session = Depends(get_db)):
    skip = (page - 1) * count
    events = crud.get_events_user(db, skip=skip, limit=count)
    return events


@events.get("/events/admin", response_model=list[schemas.Event])
def read_events_admin(page: int = 1, count: int = 25, db: Session = Depends(get_db)):
    skip = (page - 1) * count
    events = crud.get_events_admin(db, skip=skip, limit=count)
    return events


@events.post("/events/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db=db, event=event)


@events.post("/events/user/buy/", responses={204: {"model": None}}, )
async def validate_events(info: Request, db: Session = Depends(get_db)):
    uuid_request = generate_uuid()
    payload = await info.json()

    if (int(crud.get_money(db, user_id=payload["user_id"]).money)
            < int(payload["quantity"] * crud.get_event(db, event_id=payload["event_id"]).price)):
        response = Response()
        response.status_code = 400
        return {"detail": "Not enough money"}

    else:
        created_ticket = crud.create_ticket(db=db, ticket=schemas.TicketCreate(
            request_id=uuid_request,
            user_id=payload["user_id"],
            event_id=payload["event_id"],
            quantity=payload["quantity"],
            status=1))

        crud.use_money(db=db, user_id=payload["user_id"], quantity=payload["quantity"] *
                       crud.get_event(db, event_id=payload["event_id"]).price)
        crud.update_our_event_less(db=db, event_id=payload["event_id"],
                                   tickets=payload["quantity"])
        event = crud.get_event(db, created_ticket.event_id)
        send_notification(ticket=created_ticket, event=event, url="")

        response = Response()
        response.headers = {"Access-Control-Allow-Origin": "*"}

        return response
