from typing import Optional,List
from fastapi import FastAPI, Response, status,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body

from random import randrange

from sqlalchemy.orm import Session
from . import models
from .database import engine,get_db

from .routers import post, user,auth,vote

from .config import settings

#To create all the models
#models.Base.metadata.create_all(bind= engine)

app = FastAPI()

origin = ["http://www.google.com","http://127.0.0.1:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/test")
def test():
    return {"message": "CORS working!"}

@app.get("/")
def read_root():
 return {"message":"Hello World pushing the changes to the ubuntu server ,  x"}

@app.get("/sqlalchemy")
def test_post(db : Session = Depends(get_db)) :

  posts = db.query(models.Posts).all()
  return {"data" : posts}

  #return {"status":"success"}




