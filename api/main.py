from fastapi import Depends, FastAPI, Request
from sqlalchemy.orm import Session

import json
import requests
import uuid
from fastapi.middleware.cors import CORSMiddleware
from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_uuid():
    return str(uuid.uuid4())


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Recibe los eventos desde subscriber
@app.post("/events/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db=db, event=event)


@app.post("/requests/", response_model=schemas.Request)
def create_request(event: schemas.RequestCreate, db: Session = Depends(get_db)):
    return crud.create_request(db=db, event=event)


# Muestra los eventos en el front
@app.get("/events/", response_model=list[schemas.Event])
def read_events(page: int = 0, count: int = 25, db: Session = Depends(get_db)):
    # skip: int = 0, limit: int = 100
    skip = (page - 1) * count
    events = crud.get_events(db, skip=skip, limit=count)
    return events


# Desde el front recibe el id del evento y la cantidad de entradas que quieren comprar
# Los envía a publisher para que valide la compra
@app.post("/events/buy/")
async def validate_events(info: Request, db: Session = Depends(get_db)):
    uuid_request = generate_uuid()
    payload = await info.json()
    crud.create_ticket(db=db, ticket=schemas.TicketCreate(request_id=uuid_request,
                                                          user_id=payload["user_id"],
                                                          event_id=payload["event_id"],
                                                          quantity=payload["quantity"],
                                                          status=2))
    # Crear base de datos par guardar la request con el user id tmbn

    validation_info = {
        "request_id": uuid_request,
        "group_id": 20,
        "event_id": payload["event_id"],
        "deposit_token": "",
        "quantity": payload["quantity"],
        "seller": 0,
    }
    requests.post(
        "http://publisher:8000/requests_create/",
        headers={"Content-type": "application/json"},
        json=json.dumps(validation_info)
    )


# Recibe TODAS las validaciones y en el caso de que sea valida
@app.post("/validations/")
async def check_validation(validations: Request, db: Session = Depends(get_db)):
    payload = await validations.json()
    # si se aprueba la validacion se tiene que modificar la cantidad de entradas
    if payload["valid"]:
        request = crud.get_request(db, payload['request_id'])
        # De esta request se obtiene el id del evento y la cantidad de entradas vendidas
        # Se las resto al evento en cuestión
        crud.update_event(db, request.event_id, request.quantity)

        # If grupo payload['group_id'] == 20
        if payload['group_id'] == 20:
            crud.update_ticket(db, request_id=payload['request_id'], status=1)
    elif not payload["valid"]:
        crud.update_ticket(db, request_id=payload['request_id'], status=0)
    return


# Muestra tickets del usuario en espera
@app.get("/tickets_user/", response_model=list[schemas.Ticket])
def read_tickets(user_id=str, status=int, db: Session = Depends(get_db)):
    tickets = crud.get_tickets_user(db, user_id=user_id, status=status)
    return tickets
