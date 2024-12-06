import json
from fastapi import Request, APIRouter, Depends
import requests
from db.get import get_db
from db import crud, schemas
from sqlalchemy.orm import Session
import uuid


auctions = APIRouter()


def generate_uuid():
    return str(uuid.uuid4())


@auctions.get("/auctions/")
def read_auctions(db: Session = Depends(get_db)):
    auctions = crud.get_auction(db)
    return auctions


# modificar a mis auctions no las de todos
@auctions.get("/auctions/proposals/")
def read_auctions_waiting(db: Session = Depends(get_db)):
    auctions = crud.get_others_proposals_to_my_offers(db)
    return auctions  # despues de ver todas las que
    # me llegan a mis auctions offfer las apruebo o rechazo


@auctions.get("/auctions/myproposals/accepted")
def get_my_proposals_accepted(db: Session = Depends(get_db)):
    auctions = crud.get_my_proposals_accepted(db)
    return auctions


@auctions.get("/auctions/myproposals/rejected")
def get_my_proposals_rejected(db: Session = Depends(get_db)):
    auctions = crud.get_my_proposals_rejected(db)
    return auctions


@auctions.get("/auctions/myproposals/")
def get_my_proposals(db: Session = Depends(get_db)):
    auctions = crud.get_my_proposals(db)
    return auctions


@auctions.get("/auctions/offers/")
def read_auctions_groups(db: Session = Depends(get_db)):
    auctions = crud.get_offers_of_other_groups(db)
    return auctions  # despues de verlas puedo enviar una oferta (proposal)


@auctions.get("/auctions/myoffers/")
def get_my_offers(db: Session = Depends(get_db)):
    auctions = crud.get_my_offers(db)
    return auctions


@auctions.get("/auctions/myoffers/accepted")
def get_my_offers_accepted(db: Session = Depends(get_db)):
    auctions = crud.get_my_offers_accepted(db)
    return auctions


@auctions.get("/auctions/myoffers/rejected")
def get_my_offers_rejected(db: Session = Depends(get_db)):
    auctions = crud.get_my_offers_rejected(db)
    return auctions


@auctions.post("/auctions/")
async def create_auction(auction: Request, db: Session = Depends(get_db)):
    payload = await auction.json()
    if (payload["group_id"] != 20):
        if (payload["type"] == "proposal"):
            crud.create_proposal(db=db, proposal=schemas.ProposalCreate(**payload))

        elif (payload["type"] == "offer"):
            crud.create_offer(db=db, offer=schemas.OfferCreate(**payload))

        elif (payload["type"] == "acceptance"):
            crud.acceptance(db=db, auction_id=payload["auction_id"], proposal_id=payload["proposal_id"])
            crud.add_assigned(db=db, event_id=payload["event_id"], quantity=payload["quantity"])

        elif (payload["type"] == "rejection"):
            crud.rejection(db=db, auction_id=payload["auction_id"], proposal_id=payload["proposal_id"])


@auctions.post("/auctions/proposal/")
async def proposal_auction(info: Request, db: Session = Depends(get_db)):
    uuid_payload = generate_uuid()
    payload = await info.json()
    request_info = {
            "auction_id": payload["auction_id"],
            "proposal_id": uuid_payload,
            "event_id": payload["event_id"],
            "quantity": payload["quantity"],
            "group_id": payload["group_id"],
            "type": "proposal"
        }
    crud.create_proposal(db=db, proposal=schemas.ProposalCreate(**request_info))
    requests.post(
        "http://publisher:8000/auction_offer/",
        headers={"Content-type": "application/json", "Access-Control-Allow-Origin": "*"},
        json=json.dumps(request_info)
    )


@auctions.post("/auctions/validate/")
async def validate_auction(info: Request, db: Session = Depends(get_db)):
    payload = await info.json()
    request_info = {
            "auction_id": payload["auction_id"],
            "proposal_id": payload["proposal_id"],
            "event_id": payload["event_id"],
            "quantity": payload["quantity"],
            "group_id": 20,
            "type": payload["type"]  # answer: acceptance or rejection
        }

    if (payload["type"] == "acceptance"):
        crud.acceptance(db=db, auction_id=payload["auction_id"], proposal_id=payload["proposal_id"])
        crud.less_assigned(db=db, event_id=payload["event_id"], quantity=payload["quantity"])
    elif (payload["type"] == "rejection"):
        crud.rejection(db=db, auction_id=payload["auction_id"], proposal_id=payload["proposal_id"])

    requests.post(
        "http://publisher:8000/auction_offer/",
        headers={"Content-type": "application/json", "Access-Control-Allow-Origin": "*"},
        json=json.dumps(request_info)
    )


@auctions.post("/auctions/offer")
async def create_offer(offer: Request, db: Session = Depends(get_db)):
    uuid_auction = generate_uuid()
    payload = await offer.json()

    request_info = {
            "auction_id": uuid_auction,
            "proposal_id": "",
            "event_id": payload["event_id"],
            "quantity": payload["quantity"],
            "group_id": 20,
            "type": "offer"
        }
    crud.create_offer(db=db, offer=schemas.OfferCreate(**request_info))
    requests.post(
        "http://publisher:8000/auction_offer/",
        headers={"Content-type": "application/json", "Access-Control-Allow-Origin": "*"},
        json=json.dumps(request_info)
    )
