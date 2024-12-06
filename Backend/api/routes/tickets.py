from fastapi import APIRouter, Depends
from db import crud, schemas
from db.get import get_db
from sqlalchemy.orm import Session

tickets = APIRouter()


# Muestra tickets del usuario en espera
@tickets.get("/tickets_user/", response_model=list[schemas.Ticket])
def read_tickets(user_id=str, status=int, db: Session = Depends(get_db)):
    tickets = crud.get_tickets_user(db, user_id=user_id, status=status)
    return tickets
