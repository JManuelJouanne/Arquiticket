import json
from fastapi import Request, APIRouter, Depends
import requests
from db.get import get_db
from db import crud, schemas
from requests.models import Response
from sqlalchemy.orm import Session
import uuid


events = APIRouter()


def generate_uuid():
    return str(uuid.uuid4())


@events.get("/events/", response_model=list[schemas.Event])
def read_events(page: int = 1, count: int = 25, db: Session = Depends(get_db)):
    # skip: int = 0, limit: int = 100
    skip = (page - 1) * count
    events = crud.get_events(db, skip=skip, limit=count)
    return events


@events.post("/events/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db=db, event=event)


@events.post("/events/buy/", responses={204: {"model": None}}, )
async def validate_events(info: Request, db: Session = Depends(get_db)):
    uuid_request = generate_uuid()
    payload = await info.json()

    if (int(crud.get_money(db, user_id=payload["user_id"]).money)
            < int(payload["quantity"] * crud.get_event(db, event_id=payload["event_id"]).price)):
        response = Response()
        response.status_code = 400
        return {"detail": "Not enough money"}

    else:
        data = {
            "group_id": 20,
            "seller": 0,
            "event_id": payload["event_id"],
            "quantity": payload["quantity"],
            "value": crud.get_event(db, event_id=payload["event_id"]).price,
        }
        print(data)
        resp = requests.post('https://api.legit.capital/v1/payments', data=json.dumps(data))

        print(resp.status_code)

        if resp.status_code == 200:
            response_data = resp.json()
            print(response_data)

        elif resp.status_code == 400:
            error_message = resp.json()['message']
            print(error_message)

        requests.post(
            "http://job_master:8000/job",
            headers={"Content-type": "application/json", "Access-Control-Allow-Origin": "*"},
            json=resp.json()
        )

        crud.create_ticket(db=db, ticket=schemas.TicketCreate(request_id=uuid_request,
                                                              user_id=payload["user_id"],
                                                              event_id=payload["event_id"],
                                                              quantity=payload["quantity"],
                                                              status=2,
                                                              link=""))

        crud.use_money(db=db, user_id=payload["user_id"], quantity=payload["quantity"] *
                       crud.get_event(db, event_id=payload["event_id"]).price)

        request_info = {
            "request_id": uuid_request,
            "group_id": 20,
            "event_id": payload["event_id"],
            "deposit_token": response_data['deposit_token'],
            "quantity": payload["quantity"],
            "seller": 0,
        }

        requests.post(
            "http://publisher:8000/requests_create/",
            headers={"Content-type": "application/json", "Access-Control-Allow-Origin": "*"},
            json=json.dumps(request_info)
        )

        response = Response()
        response.headers = {"Access-Control-Allow-Origin": "*"}

        return response
