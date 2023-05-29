from . import database


def get_db():
    datab = database.SessionLocal()
    try:
        yield datab
    finally:
        datab.close()
