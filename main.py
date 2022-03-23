from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from exceptions import StoryExceotion
from router import blog_get, blog_post, user, article
from db import models
from db.database import engine

app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)


models.Base.metadata.create_all(engine)

@app.get('/')
def index():
    return {'message': 'Hello world!'}

@app.exception_handler(StoryExceotion)
def story_exception_handler(request:Request, exc:StoryExceotion):
    return JSONResponse(status_code=status.HTTP_418_IM_A_TEAPOT, content={"Error":exc.name})

# @app.exception_handler(HTTPException)
# def custome_handler(request:Request, exc:StoryExceotion):
#     return PlainTextResponse(str(exc), status_code=400)