
from typing import Optional,List
from fastapi import FastAPI, Response, status,HTTPException,Depends,APIRouter
from .. import models, oauth2,schemas
from sqlalchemy.orm import Session
from ..database import get_db

from sqlalchemy import func

router = APIRouter(
  prefix = "/posts",
  tags = ['Posts']
)


#@router.get("/",response_model=List[schemas.Post])
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db : Session = Depends(get_db),current_user: str = Depends(oauth2.get_current_user),
              limit : int = 10, skip : int = 0,search: Optional[str] = "") :
 #pass in the SQL statement using cursor.execute()
 #cursor.execute(""" SELECT * FROM posts""")
 #run the SQL statement using cursor.fetchmany() in case of retriving multiple posts 
 #posts = cursor.fetchall()
 #Instead of retruning my_posts static array, reurn the data from the DB
 #print (posts)

 #posts = db.query(models.Posts).filter(models.Posts.owner_id == current_user.id).all()
 #posts = db.query(models.Posts).all()

 #posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()

 posts = db.query(models.Posts,func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Posts.id == models.Votes.post_id,
                                            isouter = True).group_by(models.Posts.id).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
 
 return posts

 
@router.post("/",status_code= status.HTTP_201_CREATED,response_model=schemas.Post)
#def create_post(payload: dict = Body(...)):
def create_post(post: schemas.PostCreate,db : Session = Depends(get_db),user: str = Depends(oauth2.get_current_user)):
  #current_user: str = Depends(oauth2.get_current_user)
  #post_dict = post.model_dump()
  #post_dict['id'] = randrange(0,1000000)
  #my_posts.append(post_dict)
  #return {"data" : post_dict}
  # %s ----> variable; python library psycopg2 santizies the parameters to avoid SQL injections
  # such as inserting SQL statement as stirng values
  #cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """, 
                 #(post.title, post.content, post.published))
  #new_post = cursor.fetchone()
  #Commit the above staged changes to the postgres database using the following command
  #conn.commit()
  #return {"data" :new_post }
  
  #new_post = models.Posts(title = post.title, content = post.content, published = post.published)

  new_post = models.Posts(owner_id = user.id, **post.model_dump())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)

  #return {"data" : new_post}
  print (user.email)
  return new_post


#@router.get("/{id}",response_model=schemas.Post)
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id : int, response: Response,db : Session = Depends(get_db),current_user: str = Depends(oauth2.get_current_user)) :
  #post = find_post(id)
  #cursor.execute(""" SELECT * from posts WHERE id = %s""", str(id,))
  #post = cursor.fetchone()
  #print(test_post)

  #post_query = db.query(models.Posts).filter(models.Posts.id == id)
  #print(post_query)

  #post = db.query(models.Posts).filter(models.Posts.id == id).first()

  post = db.query(models.Posts,func.count(models.Votes.post_id).label("votes")).join(models.Votes, 
                   models.Posts.id == models.Votes.post_id, 
                   isouter = True).group_by(models.Posts.id).filter(models.Posts.id == id).first()

  if not post :
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail = f"post with id {id} was not found")
  
  #return {"post_detail" : post}

  #if post.owner_id != current_user.id :
  #  raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
  #                      detail = f"Not authorized to perform the requested action")


  return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db : Session = Depends(get_db),current_user: str = Depends(oauth2.get_current_user)) :
  #cursor.execute("""DELETE from posts where id = %s returning * """, str(id,))
  #deleted_post = cursor.fetchone()
  #conn.commit()


  #index = find_index_post(id)
  #if index == None :

  post_query = db.query(models.Posts).filter(models.Posts.id == id)

  post = post_query.first()

  #if deleted_post == None :
  if post == None :
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail = f"post with the id {id} was not found")
  #my_posts.pop(index)

  if post.owner_id != current_user.id :
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail = f"Not authorized to perform the requested action")

  post_query.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}",response_model=schemas.Post)
def update_post(id : int, updated_post_py_model: schemas.PostCreate,db : Session = Depends(get_db),current_user: str = Depends(oauth2.get_current_user)) :
  #cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning * """,
  #(post.title, post.content, post.published,str(id,)))
  #pdated_post = cursor.fetchone()
  #conn.commit()

  #print(post)
  #index = find_index_post(id)
  #if index == None :

  post_query = db.query(models.Posts).filter(models.Posts.id == id)

  post = post_query.first() 


  #if updated_post == None :
  if post == None :
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail = f"post with the id {id} was not found")
  
  if post.owner_id != current_user.id :
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail = f"Not authorized to perform the requested action")
  
  post_query.update(updated_post_py_model.model_dump(),
              synchronize_session=False)
  db.commit()
  
  #post_dict = post.model_dump()
  #post_dict["id"] = id
  #my_posts[index] = post_dict
  
  #return {"data":post_dict}
  #return {"data" : updated_post}

  #return {"data" : post_query.first() }
  return post_query.first() 
