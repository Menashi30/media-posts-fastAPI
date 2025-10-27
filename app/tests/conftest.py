import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  sessionmaker

from fastapi.testclient import TestClient
from app.main import app


from app.config import settings
from app.database import get_db
from app.database import Base

from app.oauth2 import create_access_token
from app import models

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

@pytest.fixture
def test_user(client) :
    user_data = {"email":"menashi30@gmail.com",
                 "password":"pswd123"}
    res = client.post("/users",json = user_data)
    #print(res.json())
    #assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user2(client) :
    user_data = {"email":"sanjeev@gmail.com",
                 "password":"xyz"}
    res = client.post("/users",json = user_data)
    #print(res.json())
    #assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user) :
   return create_access_token({'user_id':test_user['id']})

@pytest.fixture
def authorized_client(client,token) :
   client.headers = {
      **client.headers,
      'Authorization' : f'Bearer {token}' 
   }

   return client

@pytest.fixture
def test_posts(test_user,session,test_user2) :
  posts_data =  [{
  "title" :"first post",
  "content" :"my first post",
  "owner_id" : test_user['id']
  },  {
  "title" :"second post",
  "content" :"my second post",
  "owner_id" : test_user['id']
  }, {
  "title" :"third post",
  "content" :"my third post",
  "owner_id" : test_user['id']
  }, {
  "title" :"fourth post",
  "content" :"my fourth post",
  "owner_id" : test_user2['id']
  }]

  def create_posts_models(post) :
    return models.Posts(**post)

  posts_map = map(create_posts_models,posts_data)

  list_post_models = list(posts_map)

  session.add_all(list_post_models)

  # session.add_all([models.Posts(title ="first post",content="my first post",owner_id=test_user['id']),
  #                  models.Posts(title ="second post",content="my second post",owner_id=test_user['id']),
  #                  models.Posts(title ="third post",content="my third post",owner_id=test_user['id'])])

  session.commit()

  posts = session.query(models.Posts).all()
  return posts
