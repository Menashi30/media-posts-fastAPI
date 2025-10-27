from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String,Boolean, text
from sqlalchemy.orm import relationship

class Posts(Base) : 
    __tablename__ = "Posts"
    
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='TRUE', nullable= False)
    created_at = Column(TIMESTAMP(timezone = 'True'), server_default = text('now()'),nullable = False)

    owner_id = Column(Integer, ForeignKey("Users.id",ondelete="CASCADE"),nullable=False)
    phone_number = Column(Integer,nullable=True)
    #add reference to another class Users with the foreign key relationship to another table
    owner = relationship("Users")

class Users(Base) :
    __tablename__ = "Users"

    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String, unique = True,nullable = False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone = 'True'), server_default = text('now()'),nullable = False)

class Votes(Base) :

    __tablename__ = "Votes"

    user_id = Column(Integer, ForeignKey("Users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer, ForeignKey("Posts.id",ondelete="CASCADE"),primary_key=True)