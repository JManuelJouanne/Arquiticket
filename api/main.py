from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine
from router import router
from sqlalchemy_utils import drop_database, create_database
from db import models

# drop_database(engine.url)
# create_database(engine.url)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
