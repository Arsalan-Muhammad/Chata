from fastapi.testclient import TestClient
from .. import app
from ..app.main import App
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
import pytest
from app import models
from app.auth import create_access_token
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port }/{settings.database_name}-test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db(): 
    db = TestSessionLocal()
    try:
            yield db
    finally:
            db.close()

App.dependency_overrides[get_db] = override_get_db
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestSessionLocal()
    try:
            yield db
    finally:
            db.close()

@pytest.fixture()
def client(session):
    def override_get_db(): 
        try:
            yield session
        finally:
            session.close()
    App.dependency_overrides[get_db] = override_get_db
    yield TestClient(App)

@pytest.fixture
def test_user(client):
    user_data = {
        "email": "helloworld@gmail.com",
        "password": "123"
    }

    res = client.post("/users/", json=user_data)

    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user

@pytest.fixture
def token(client , test_user):
     return create_access_token({"user_id" : test_user['id']})

@pytest.fixture
def authorized_client(client , test_user , token):
     
     client.headers = {
          "Authorization" : f"Bearer {token}"
     }

     return client

@pytest.fixture
def test_posts(session , test_user):
     posts_data = [{
          "title" : "first title",
          "content" : "first content",
          "owner_id" : test_user['id']
     },
     {
          "title" : "second title",
          "content" : "second content",
          "owner_id" : test_user['id']
     },
     {
          "title" : "third title",
          "content" : "third content",
          "owner_id" : test_user['id']
     }]

     def create_post_model(post):
          return models.Post(**post)
     
     posts_map = map(create_post_model , posts_data)
     posts = list(posts_map)

     session.add_all(posts)
     session.commit()

     return session.query(models.Post).all()

