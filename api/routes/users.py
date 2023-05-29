from fastapi import APIRouter, Depends, Request
from db.get import get_db
from db import crud, schemas
from sqlalchemy.orm import Session


users = APIRouter()


@users.post("/user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@users.get("/user/wallet", response_model=schemas.User)
def get_money(user_id: str, db: Session = Depends(get_db)):
    user_wallet = crud.get_money(db, user_id=user_id)
    return user_wallet


@users.post("/user/wallet")
async def add_money(info: Request, db: Session = Depends(get_db)):
    payload = await info.json()
    crud.add_money(db, payload['user_id'], payload['quantity'])
    return
