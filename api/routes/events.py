from fastapi import Request, APIRouter, Depends
from db.get import get_db
from db import crud, schemas
from mailing import send_notification
from requests.models import Response
from sqlalchemy.orm import Session
import uuid
import boto3
import json


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


@events.post("/events/user/buy/", responses={204: {"model": None}})
async def validate_events(info: Request, db: Session = Depends(get_db)):
    uuid_request = generate_uuid()
    payload = await info.json()

    if (int(crud.get_money(db, user_id=payload["user_id"]).money)
            < int(payload["quantity"] * int(crud.get_event(db, event_id=payload["event_id"]).price))):
        response = Response()
        response.status_code = 400
        return {"detail": "Not enough money"}

    else:
        created_ticket = crud.create_ticket(db=db, ticket=schemas.TicketCreate(
            request_id=uuid_request,
            user_id=payload["user_id"],
            event_id=payload["event_id"],
            quantity=payload["quantity"],
            status=1,
            link=""
        ))

        crud.use_money(db=db, user_id=payload["user_id"], quantity=payload["quantity"] *
                       crud.get_event(db, event_id=payload["event_id"]).price)
        crud.update_our_event_less(db=db, event_id=payload["event_id"],
                                   tickets=payload["quantity"])
        # Mailing
        ticket = crud.get_ticket(db, uuid_request)
        event = crud.get_event(db, payload["event_id"])
        # lambda
        data = {
            "name": event.name,
            "user": ticket.user_id,
            "date": event.date,
            "id": event.event_id,
            "request_id": ticket.request_id,
        }
        session = boto3.Session(
            region_name='us-east-2',
            aws_access_key_id='AKIAWTW2MNNWBVCCU3QL',
            aws_secret_access_key='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'
        )

        lambda_client = session.client('lambda')

        response = lambda_client.invoke(
            FunctionName='generar_ticket',
            Payload=json.dumps(data)
        )

        result = response['Payload'].read().decode('utf-8')
        result = json.loads(result)["body"]

        crud.update_ticket_link(db, request_id=uuid_request, link=result["url"])
        # URL para descargar las entradas de AWS Lambda
        url = result["url"].replace(" ", "")
        send_notification(ticket=ticket, event=event, url=url)

        response = Response()
        response.headers = {"Access-Control-Allow-Origin": "*"}

        return response
