from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  sessionmaker

import psycopg2;
from psycopg2.extras import  RealDictCursor;
import time;
from .config import settings

#SQLALCHEMEY_DATABASE_URL =  "postgresql://postgres:postgres@localhost/fastapi"

SQLALCHEMEY_DATABASE_URL =  f'postgresql://{settings.
database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMEY_DATABASE_URL)

# we want to make use of a session when we actaully want to talk to the database

SesionLocal = sessionmaker(autocommit = False, autoflush=False, bind= engine)

Base = declarative_base()

#Create the following dependency which opens up a new session upon connection to the 
# database whenever we get a request and close the db when the query is done
# we can keep calling this function whenever we get a request to any of our API endpoints

 
def get_db() :
  db = SesionLocal()
  try :
    yield db
  finally :
    db.close()


# while True:
#         try:
#           conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',
#                           password='postgres',cursor_factory=RealDictCursor)
#           cursor = conn.cursor()
#           print("Connection to the database was successfull")
#           break
#         except Exception as error:
#           print("Connection to the database was failed")
#           print("Error :",error)
#           time.sleep(2)