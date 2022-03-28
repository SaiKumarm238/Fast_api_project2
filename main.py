from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from exceptions import StoryException
from router import blog_get, blog_post, user, article, file, product
from auth import authentication
from templates import templates
from db import models
from db.database import engine
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import time
from client import html
from fastapi.websockets import WebSocket



#App Instaliation 
app = FastAPI()

#Include Routers
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(templates.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(file.router)

#Data Base
models.Base.metadata.create_all(engine)

#mount the templates, static, FIles 
app.mount('/files', StaticFiles(directory="files"), name='files')
app.mount('/templates/static', StaticFiles(directory="templates/static"), name='static')

#Middlewares
@app.middleware('http')
async def add_middleware(request: Request, call_next):
  start_time = time.time()
  response = await call_next(request)
  duration = time.time() - start_time
  response.headers['duration'] = str(duration)
  return response


origins = [
  'http://localhost:3000'
]

app.add_middleware(
  CORSMiddleware,
  allow_origins = origins,
  allow_credentials = True,
  allow_methods = ["*"],
  allow_headers = ['*']
)


@app.get('/home')
def index():
    return {'message': 'Hello world!'}

@app.exception_handler(StoryException)
def story_exception_handler(request:Request, exc:StoryException):
    return JSONResponse(status_code=status.HTTP_418_IM_A_TEAPOT, content={"Error":exc.name})

# @app.exception_handler(HTTPException)
# def custome_handler(request:Request, exc:StoryExceotion):
#     return PlainTextResponse(str(exc), status_code=400)

@app.get("/")
async def chat():
  return HTMLResponse(html)

clients = []

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  clients.append(websocket)
  while True:
    data = await websocket.receive_text()
    for client in clients:
      await client.send_text(data) 