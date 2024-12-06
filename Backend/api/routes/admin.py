import json
from fastapi import Request, APIRouter, Depends
import requests
from db.get import get_db
from db import crud
from requests.models import Response
from sqlalchemy.orm import Session
import uuid


admin = APIRouter()


def generate_uuid():
    return str(uuid.uuid4())


@admin.get("/wallet/")
def read_wallet():
    group_money = requests.get('https://api.legit.capital/v1/wallet/20')
    return group_money.json()["balance"]


@admin.post("/events/admin/buy/", responses={204: {"model": None}}, )
async def validate_events(info: Request, db: Session = Depends(get_db)):
    uuid_request = generate_uuid()
    payload = await info.json()
    # group_money = requests.get('https://api.legit.capital/v1/wallet/20')
    # group_money.json()["balance"]

    if (1000000
            < int(payload["quantity"] * crud.get_event(db, event_id=payload["event_id"]).price)):
        response = Response()
        response.status_code = 400
        return {"detail": "Not enough money"}

    else:
        print(payload)
        data = {
            "group_id": 20,
            "seller": 20,
            "event_id": payload["event_id"],
            "quantity": payload["quantity"],
            "value": crud.get_event(db, event_id=payload["event_id"]).price,
        }
        resp = requests.post('https://api.legit.capital/v1/payments', data=json.dumps(data))

        if resp.status_code == 200:
            response_data = resp.json()

        requests.post(
            "http://job_master:8000/job",
            headers={"Content-type": "application/json", "Access-Control-Allow-Origin": "*"},
            json=resp.json()
        )

        request_info = {
            "request_id": uuid_request,
            "group_id": 20,
            "event_id": payload["event_id"],
            "deposit_token": response_data['deposit_token'],
            "quantity": payload["quantity"],
            "seller": 20,
        }

        requests.post(
            "http://publisher:8000/requests_create/",
            headers={"Content-type": "application/json", "Access-Control-Allow-Origin": "*"},
            json=json.dumps(request_info)
        )

        response = Response()
        response.headers = {"Access-Control-Allow-Origin": "*"}

        return response
