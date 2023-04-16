from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/events/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db=db, event=event)


@app.get("/events/", response_model=list[schemas.Event])
def read_events(page: int = 0, count: int = 25, db: Session = Depends(get_db)):
    # skip: int = 0, limit: int = 100
    skip = (page - 1) * count
    events = crud.get_events(db, skip=skip, limit=count)
    return events
