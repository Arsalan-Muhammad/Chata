from sqlalchemy import Column, Integer, String, false
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:arsalan%40512@localhost:5432/Notes_app"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()