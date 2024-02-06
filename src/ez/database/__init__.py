import os
import ez
from ez.events import App
from sqlalchemy import *
from sqlalchemy.orm import Session


engine = create_engine(os.environ.get("DATABASE_URL"))
session = Session(engine)


@ez.on(App.DidStart)
def close_session():
    global session, engine

    session.close()
    engine.dispose()

    engine = create_engine(os.environ.get("DATABASE_URL"))
    session = Session(engine)
