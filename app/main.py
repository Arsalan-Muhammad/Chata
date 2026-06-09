from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine, get_db
from .routes import post , users , auths , vote
# Create tables
# models.Base.metadata.create_all(bind=engine)


app = FastAPI()
origins = ["https://www.google.com"]

@app.get("/")
def home():
    return {"meassage" : "Welcome to Home Page"}
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(post.router)
app.include_router(users.router)
app.include_router(auths.router)
app.include_router(vote.router)