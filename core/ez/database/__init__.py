import os
import ez
from ez.events import App
from sqlalchemy import *
from sqlalchemy.orm import Session
# import logging

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)
session = Session(engine)


@ez.on(App.DidStart)
def close_session():
    global session, engine

    session.close()
    engine.dispose()

    engine = create_engine(DATABASE_URL)
    session = Session(engine)

    ez.log.info("Database connected")
