
from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine, get_db
from .routes import post , users , auths , vote
# Create tables
# models.Base.metadata.create_all(bind=engine)


App = FastAPI()
origins = ["https://www.google.com"]

@App.get("/")
def home():
    return {"meassage" : "Welcome to Home Page"}
App.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
App.include_router(post.router)
App.include_router(users.router)
App.include_router(auths.router)
App.include_router(vote.router)