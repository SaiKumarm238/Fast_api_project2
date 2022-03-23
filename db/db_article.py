from exceptions import StoryExceotion
from db.models import DBArtical
from db.schemas import AricalBase, Artical, AricalDisplay
from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status

def create_article(db:Session, request:AricalBase):
    if request.content.startswith("Once upon a time"):
        raise StoryExceotion('No Stories Please')
    new_artic = DBArtical(title= request.title, content =request.content, published= request.published, user_id = request.creator_id)
    db.add(new_artic)
    db.commit()
    db.refresh(new_artic)
    return new_artic

def get_articale(db:Session, id:int):
    artical = db.query(DBArtical).filter(DBArtical.id == id).first()
    if not artical:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article with id {id} not found")
    return artical