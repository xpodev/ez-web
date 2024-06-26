import ez
from ez.site import CONFIG
from sqlalchemy import *
from sqlalchemy.orm import Session

engine = create_engine(CONFIG.database.uri, pool_recycle=3600)
session = Session(engine)

@ez.events.on("App.Started")
def close_session():
    global session, engine

    session.close()
    engine.dispose()

    engine = create_engine(CONFIG.database.uri, pool_recycle=3600)
    session = Session(engine)

    ez.log.info("Database connected")
