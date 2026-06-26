from app import schemas
import pytest

from tests.conftest import authorized_client
def test_get_all_posts(authorized_client , test_posts):
    res = authorized_client.get("/posts/")
    print(res.json())

    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client , test_user , test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_posts(client , test_user , test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401 


def test_user_get_one_posts_does_not_exist(authorized_client , test_user):
    res = authorized_client.get(f"/posts/888")

    assert res.status_code == 404


def test_get_one_post(authorized_client , test_posts , test_user):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")  
    Post = schemas.PostOut(**res.json()[0])
    assert Post.Post.id == test_posts[0].id

@pytest.mark.parametrize("title , content , published",[
    ("awesome_new_title" , "new_content" , True)
])    
def test_create_one_post(authorized_client , test_user , test_posts , title , content , published):
    res = authorized_client.post("/posts" , json={"title" : title , "content" : content , "published" : published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content

def test_unauthorized_user_create_posts(client , test_posts , test_user):
    res = res = client.post("/posts" , json={"title" : "title" , "content" : "content" , "published" : "published"})
    assert res.status_code == 401

    
def test_unauthorized_user_delete_posts(client , test_posts , test_user):
    res =  client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_user_delete_posts_sucees(authorized_client , test_posts , test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204   

def test_user_delete_post_not_found(authorized_client , test_posts , test_user):
    res = authorized_client.delete(f"/posts/800")
    assert res.status_code == 404
