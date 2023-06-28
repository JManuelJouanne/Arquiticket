from sqlalchemy.orm import Session

from db import schemas
from . import models


def get_event(db: Session, event_id: str):
    return db.query(models.Event).filter(models.Event.event_id == event_id).first()


def update_event(db: Session, event_id: str, discount: int):
    db.query(models.Event).filter(models.Event.event_id == event_id).first().quantity -= discount
    db.commit()


def update_our_event(db: Session, event_id: str, tickets: int):
    db.query(models.Event).filter(models.Event.event_id == event_id).first().assigned += tickets
    db.commit()


def update_our_event_less(db: Session, event_id: str, tickets: int):
    db.query(models.Event).filter(models.Event.event_id == event_id).first().assigned -= tickets
    db.commit()


def get_events_user(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).filter(models.Event.assigned > 0).offset(skip).limit(limit).all()


def get_events_admin(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).filter(models.Event.assigned == 0).offset(skip).limit(limit).all()


def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def create_offer(db: Session, offer: schemas.OfferCreate):
    db_offer = models.Offer(**offer.dict())
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer


def create_proposal(db: Session, proposal: schemas.ProposalCreate):
    db_proposal = models.Proposal(**proposal.dict())
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return db_proposal


def get_auction(db: Session):
    results = []
    results += db.query(models.Offer).all()
    results += db.query(models.Proposal).all()
    return results


def acceptance(db: Session, auction_id: str, proposal_id: str):
    db.query(models.Offer).filter(models.Offer.auction_id == auction_id).first().status = 1
    db.commit()
    proposals = db.query(models.Proposal).filter(models.Proposal.auction_id == auction_id,
                                                 models.Proposal.proposal_id != proposal_id).all()
    for proposal in proposals:
        proposal.status = 0
    db.commit()

    db.query(models.Proposal).filter(models.Proposal.auction_id == auction_id,
                                     models.Proposal.proposal_id == proposal_id).first().status = 1
    db.commit()


def rejection(db: Session, auction_id: str, proposal_id: str):
    db.query(models.Proposal).filter(models.Proposal.auction_id == auction_id,
                                     models.Proposal.proposal_id == proposal_id).all().status = 0
    db.commit()


def add_assigned(db: Session, event_id: str, quantity: int):
    db.query(models.Event).filter(models.Event.event_id == event_id).first().assigned += quantity
    db.commit()


def less_assigned(db: Session, event_id: str, quantity: int):
    db.query(models.Event).filter(models.Event.event_id == event_id).first().assigned -= quantity
    db.commit()


def get_offers_of_other_groups(db: Session):
    return db.query(models.Offer).filter(models.Offer.status == 2,
                                         models.Offer.type == "offer",
                                         models.Offer.group_id != 20).all()


def get_my_offers(db: Session):
    return db.query(models.Offer).filter(models.Offer.status == 2,
                                         models.Offer.type == "offer",
                                         models.Offer.group_id == 20).all()


def get_my_offers_accepted(db: Session):
    return db.query(models.Offer).filter(models.Offer.status == 1,
                                         models.Offer.group_id == 20).all()


def get_my_offers_rejected(db: Session):
    return db.query(models.Offer).filter(models.Offer.status == 0,
                                         models.Offer.group_id == 20).all()


def get_my_proposals(db: Session):
    return db.query(models.Proposal).filter(models.Proposal.status == 2,
                                            models.Proposal.type == "proposal",
                                            models.Proposal.group_id == 20).all()


def get_my_proposals_accepted(db: Session):
    return db.query(models.Proposal).filter(models.Proposal.status == 1,
                                            models.Proposal.group_id == 20).all()


def get_my_proposals_rejected(db: Session):
    return db.query(models.Proposal).filter(models.Proposal.status == 0,
                                            models.Proposal.group_id == 20).all()


def get_others_proposals_to_my_offers(db: Session):
    my_offers = get_my_offers(db)
    results = []
    for offer in my_offers:
        auction_id = offer.auction_id
        matching_proposal = db.query(models.Proposal).filter(models.Proposal.auction_id == auction_id,
                                                             models.Proposal.group_id != 20,
                                                             models.Proposal.type == "proposal").all()
        if matching_proposal:
            results.append(matching_proposal)
    return results


def get_request(db: Session, request_id: str):
    return db.query(models.Request).filter(models.Request.request_id == request_id).first()


def get_requests_user(db: Session, user_id: str):
    return db.query(models.Request).filter(models.Request.user_id == user_id).all()


def create_request(db: Session, event: schemas.RequestCreate):
    db_request = models.Request(**event.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def get_ticket(db: Session, request_id: str):
    return db.query(models.Ticket).filter(models.Ticket.request_id == request_id).first()


def get_tickets_user(db: Session, user_id: str, status: int):
    return db.query(models.Ticket).filter(models.Ticket.user_id == user_id,
                                          models.Ticket.status == status).all()


def create_ticket(db: Session, ticket: schemas.TicketCreate):
    db_ticket = models.Ticket(**ticket.dict())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def update_ticket(db: Session, request_id: str, status: int):
    db.query(models.Ticket).filter(models.Ticket.request_id == request_id).first().status = status
    db.commit()


def update_ticket_link(db: Session, request_id: str, link: str):
    db.query(models.Ticket).filter(models.Ticket.request_id == request_id).first().link = link
    db.commit()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: str):
    db.query(models.User).filter(models.User.user_id == user_id).first().admin = True
    db.commit()


def get_money(db: Session, user_id: str):
    print(" d")
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def add_money(db: Session, user_id: str, quantity: int):
    db.query(models.User).filter(models.User.user_id == user_id).first().money += quantity
    db.commit()


def use_money(db: Session, user_id: str, quantity: int):
    db.query(models.User).filter(models.User.user_id == user_id).first().money -= quantity
    db.commit()
