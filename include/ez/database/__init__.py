import ez
from ez.site import CONFIG
from ez.events import App
from sqlalchemy import *
from sqlalchemy.orm import Session
# import logging

engine = create_engine(CONFIG.database.uri, pool_recycle=3600)
session = Session(engine)

@ez.events.on(App.DidStart)
def close_session():
    global session, engine

    session.close()
    engine.dispose()

    engine = create_engine(CONFIG.database.uri, pool_recycle=3600)
    session = Session(engine)

    ez.log.info("Database connected")
