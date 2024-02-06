import os
from sqlalchemy import *
from sqlalchemy.orm import Session
# import logging


engine = create_engine(os.environ.get('DATABASE_URL'))
session = Session(engine)

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)