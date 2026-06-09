
from .. import models , schemas , ultis , auth
from fastapi import FastAPI, HTTPException, status, Depends , APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List , Optional
from sqlalchemy import func
router = APIRouter(
    tags=['Posts']
)
@router.get("/posts", response_model=List[schemas.PostOut])
def get_posts(
                db: Session = Depends(get_db),
                current_user = Depends(auth.get_current_user),
                Limit:int = 15,
                skip: int = 0,
                search: Optional[str] = ""
              ):

    result = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote,
        models.Vote.post_id == models.Post.id,
        isouter=True
    ).group_by(models.Post.id).filter(
        models.Post.title.contains(search)
    ).offset(skip).limit(Limit).all()

    return result
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CREATE,db: Session = Depends(get_db),current_user = Depends(auth.get_current_user)):


    new_post = models.Post( owner_id=current_user.id , **post.dict()
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/posts/{id}", response_model=list[schemas.PostOut])
def get_post(id: int, db: Session = Depends(get_db),current_user = Depends(auth.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    
    result = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote,
        models.Vote.post_id == models.Post.id,
        isouter=True

    ).group_by(models.Post.id).filter(models.Post.id == id)


    
    return result


@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.CREATE, db: Session = Depends(get_db) ,  current_user = Depends(auth.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not Authorized To Perform The Requested action")

    post_query.update(updated_post.dict(), synchronize_session=False) #pyright: ignore 
    db.commit()

    return post_query.first()

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not Authorized To Perform The Requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return "Post is deleted Succesfully"