from pydantic import BaseModel, EmailStr,Field
from  datetime import datetime 
from typing import Optional,Annotated

from pydantic.types import conint

class PostBase (BaseModel) :
  title: str
  content: str
  published: bool = True
  #rating: Optional[int] = None
  phone_number: int

class PostCreate (PostBase) :
  #same key-value as such the PostBase class
  pass 

#schema for the user created response
class UserOut (BaseModel) : 
  id : int
  email : EmailStr
  created_at : datetime

#update post which allows the user to update only the published field
#class PostUpdate (BaseModel) : 
#  published: bool

#schema for the post response after adding the "owner" property
class Post (PostBase) : 
  id : int
  created_at : datetime
  owner_id : int
  owner : UserOut
  

# In case, if the pydantic model can not read ORM model which is not a dict
  #class Config :
    #orm_mode = True


class PostOut(BaseModel):
    Posts: Post
    votes: int

    class Config :
     orm_mode = True



class UserCreate (BaseModel) :
  email : EmailStr
  password : str



class UserLogin(BaseModel) :
  email : EmailStr
  password : str


class Token(BaseModel) :
  access_token : str
  token_type: str

class TokenData(BaseModel) : 
  id : int

class Vote(BaseModel) :
  post_id : int
  dir: Annotated[int, Field(ge=0, le=1)]  # dir can only be 0 or 1
  