from fastapi import APIRouter
from routes.events import events
from routes.validations import router_validations
from routes.requests import requests
from routes.tickets import tickets
from routes.users import users

router = APIRouter()


@router.get("/")
def main():
    return {"message": "Health Check Passed!"}


router.include_router(events)
router.include_router(router_validations)
router.include_router(requests)
router.include_router(tickets)
router.include_router(users)
