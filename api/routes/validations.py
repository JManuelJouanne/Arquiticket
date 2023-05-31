from fastapi import Request, APIRouter, Depends
from db import crud
from sqlalchemy.orm import Session
from db.get import get_db
from mailing import send_notification
from boto3 import Session
import json

router_validations = APIRouter()


@router_validations.post("/validations/")
async def check_validation(validations: Request, db: Session = Depends(get_db)):
    payload = await validations.json()
    # si se aprueba la validacion se tiene que modificar la cantidad de entradas
    if payload["valid"]:
        request = crud.get_request(db, payload["request_id"])
        # De esta request se obtiene el id del evento y la cantidad de entradas vendidas
        # Se las resto al evento en cuestión
        crud.update_event(db, request.event_id, request.quantity)
        # If grupo payload['group_id'] == 20
        if int(payload["group_id"]) == 20:
            crud.update_ticket(db, request_id=payload["request_id"], status=1)
            # Mailing
            ticket = crud.get_ticket(db, payload['request_id'])
            event = crud.get_event(db, ticket.event_id)
            # lambda
            data = {
                "name": event.name,
                "user": ticket.user_id,
                "date": event.date,
                "id": event.id,
                "request_id": ticket.request_id,
            }
            session = Session(
                region_name='us-east-2',
                aws_access_key_id='AKIAWTW2MNNWBVCCU3QL',
                aws_secret_access_key='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'
            )

            lambda_client = session.client('lambda')

            response = lambda_client.invoke(
                FunctionName='generar_ticket',
                Payload=json.dump(data)
            )

            result = response['Payload'].read().decode('utf-8')
            result = json.loads(result)
            # URL para descargar las entradas de AWS Lambda
            send_notification(ticket=ticket, event=event, url=result["url"])
    elif not payload["valid"] and int(payload["group_id"]) == 20:
        crud.update_ticket(db, request_id=payload["request_id"], status=0)
    return
