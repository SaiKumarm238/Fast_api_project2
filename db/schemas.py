from turtle import title
from pydantic import BaseModel
from typing import List


class Artical(BaseModel):
    title :str
    content : str
    published :bool
    class Config():
        orm_mode = True
        
#User inside ArticalDisplay
class User(BaseModel):
    id:int
    username: str
    
    class Config():
        orm_mode = True

class UserBase(BaseModel):
    username :str
    email : str
    password :str
    
class UserDisplay(BaseModel):
    username : str
    email : str
    items : List[Artical] = []
    
    class Config():
        orm_mode = True
        
class AricalBase(BaseModel):
    title : str
    content : str
    published : bool
    creator_id: int
    
    
class AricalDisplay(BaseModel):
    title : str
    content : str
    published : bool
    user: User
    
    class Config():
        orm_mode = True
    
    
