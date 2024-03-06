import ez
from ez.config import config
from ez.events import App
from sqlalchemy import *
from sqlalchemy.orm import Session
# import logging

engine = create_engine(config.database.uri, pool_recycle=3600)
session = Session(engine)

@ez.on(App.DidStart)
def close_session():
    global session, engine

    session.close()
    engine.dispose()

    engine = create_engine(config.database.uri, pool_recycle=3600)
    session = Session(engine)

    ez.log.info("Database connected")
