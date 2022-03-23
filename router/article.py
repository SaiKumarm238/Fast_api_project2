from typing import List
from fastapi import APIRouter, Depends
from db.schemas import Artical, AricalBase, AricalDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_article


router = APIRouter(
    prefix='/article',
    tags=['Article']
)

#get the article based on id
@router.get('/{id}', response_model=AricalDisplay)
def get_artical(id:int, db:Session = Depends(get_db)):
    return db_article.get_articale(db, id)

#create article
@router.post('/', response_model=AricalDisplay)
def create_article(request:AricalBase ,db:Session = Depends(get_db)):
    return db_article.create_article(db, request)