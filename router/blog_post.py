from fastapi import APIRouter, Body, Query, Path
from pydantic import BaseModel
from typing import Optional, List, Dict
router = APIRouter(
    prefix='/blog',
    tags=['Blog']
)

class Image(BaseModel):
    url :str
    alias :str

class BlogModel(BaseModel):
    title :str
    content :str
    no_coments :int
    published : Optional[bool]
    tags: List[str] = []
    metadata : Dict[str,str] = {'key1':'val1'}
    image: Optional[Image] = None


@router.post('/new/{id}')
def create_blog(blog:BlogModel, id:int, version: int =1):
    return {
        "id":id,
        "data":blog,
        "version":version
        }
    
@router.post('/new/{id}/comment/{comment_id}')
def create_comment(blog:BlogModel,id:int,
                   comment_title:str = Query(None, 
                                            title="Title of the Comment",
                                            description="Some description for comment_title",
                                            alias="commentTitle", deprecated=True),
                   content:str =Body(..., min_length=10, max_length=50,regex='^[a-z\s]*$'),
                   v: Optional[List[str]]= Query(["1.0", "1.1","1.2"]),
                   comment_id: int = Path(None, gt=5)
                   ):
    return {
        "blog":blog,
        "id":id,
        "comment_title":comment_title,
        'content':content,
        'version':v,
        "comment_id":comment_id,
    }
    
    
def required_functionality():
    return {'message':'Learning FastAPI is important'}