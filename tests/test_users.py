
import pytest
from app import schemas
from app import config
from jose import JWTError , jwt

def test_create_user(client):
       res = client.post("/users/" , json={"email" : "hello123@gmail.com" , "password" : "a@15"})
       assert res.status_code == 201

def test_login_user(client , test_user):
       res = client.post("/login" , data={"username" : test_user['email'] , "password" : test_user['password']})
       login_res = schemas.Token(**res.json())
       payload = jwt.decode(login_res.access_token , config.settings.secret_key , config.settings.algorithm)

       id = payload.get("user_id") #pyright:ignore reportArgumentTyp
       assert id == test_user['id']
       assert login_res.token_type == "bearer"
       assert res.status_code == 200

@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("hello123@gmail.com", "wrongpassword", 403),
        ("wrongemail", "a@15", 403)
    ]
)
def test_failed_login(test_user , client  , email , password , status_code):
       res = client.post(
              "/login" , data={"username" : email , "password" : password}
       )

       assert res.status_code == status_code



