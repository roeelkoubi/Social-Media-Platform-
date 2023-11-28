from .. import models,schemas,utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .. database import engine,get_db
from sqlalchemy.orm import Session
from .. import oauth2

router = APIRouter(prefix = "/posts")

# my_posts = [{"title": "title of post 1", "content": "content of post 1","id": 1},{"title":"favorite foods","content":"I like pizza","id":2}]

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
        
# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i
    
# @router.get("/")
# def root():
#     return {"message": "Hello World!"} 

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data":"successfull"}
    
@router.get("/")
def get_posts(db: Session = Depends(get_db),response_model=schemas.Post,get_current_user : int = Depends(oauth2.get_current_user),limit : int = 10,skip : int = 0,
              search : Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # my_posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts 

@router.post("/",status_code = status.HTTP_201_CREATED,response_model=schemas.Post) # Defulat status code 
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db),get_current_user : int = Depends(oauth2.get_current_user)): # Validate post look like the schmeme that will define up.
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """, (post.title,post.content,post.published))
    # new_posts = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id = get_current_user.id,**post.dict())
    # new_post = models.Post(title = post.title,content = post.content, published = post.published)
    db.add(new_post)
    db.commit() 
    db.refresh(new_post)
    return new_post

# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail": post}

@router.get("/{id}")
def get_post_by_id(id: int,db: Session = Depends(get_db),resonse_model = schemas.Post,get_current_user : int = Depends(oauth2.get_current_user)): 
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id {id} not found"}
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post (id:int, updated_post: schemas.PostCreate,db: Session = Depends(get_db),resonse_model = schemas.Post,get_current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s,content = %s, published = %s WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = f"post with id {id} not found")
    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = "NOT AUTORIZED")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return updated_post
    # return {'message':updated_post}
    