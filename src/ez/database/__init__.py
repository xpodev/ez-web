import os
from sqlalchemy import *
from sqlalchemy.orm import Session


engine = create_engine(os.environ.get('DATABASE_URL'))
session = Session(engine)