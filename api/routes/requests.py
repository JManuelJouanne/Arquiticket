from fastapi import APIRouter, Depends
from db.get import get_db
from db import crud, schemas
from sqlalchemy.orm import Session


requests = APIRouter()


@requests.post("/requests/", response_model=schemas.Request)
def create_request(event: schemas.RequestCreate, db: Session = Depends(get_db)):
    return crud.create_request(db=db, event=event)
