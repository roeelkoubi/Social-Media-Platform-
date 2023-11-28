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

router = APIRouter()

@router.post("/users",status_code = status.HTTP_201_CREATED,response_model=schemas.UserOut) # Defulat status code     
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    hashed_passwprd = utils.hash(user.password)
    user.password = hashed_passwprd
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit() 
    db.refresh(new_user)
    return new_user

@router.get("/users/{id}",response_model=schemas.UserOut)
def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail= "User not found")
    return user
    
    