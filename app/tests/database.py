import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  sessionmaker

from fastapi.testclient import TestClient
from app.main import app


from app.config import settings
from app.database import get_db
from app.database import Base

SQLALCHEMEY_DATABASE_URL =  "postgresql://postgres:postgres@localhost/fastapi_test"

#SQLALCHEMEY_DATABASE_URL = f'postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMEY_DATABASE_URL)

#To create all the table schemas
#the below code is in the fixture, so commeting
#Base.metadata.create_all(bind= engine)

# we want to make use of a session when we actaully want to talk to the database

TestingSesionLocal = sessionmaker(autocommit = False, autoflush=False, bind= engine)

#Base = declarative_base()

#Belowing code and swaoing the get_db() are all moved inside the fixtures, so commenting

#def override_get_db() :
#  db = TestingSesionLocal()
#  try :
#    yield db
#  finally :
#    db.close()

#app.dependency_overrides[get_db] = override_get_db

#client = TestClient(app)


@pytest.fixture()
def session() :
   #After running the test, drop all the tables
   Base.metadata.drop_all(bind= engine)
   #Before running any test case, it should create all tables.
   Base.metadata.create_all(bind= engine)
   db = TestingSesionLocal()
   try :
      yield db
   finally :
      db.close()

@pytest.fixture()
def client(session) :
  def override_get_db() :
    try :
      yield session
    finally :
      session.close()

  app.dependency_overrides[get_db] = override_get_db
  yield TestClient(app)