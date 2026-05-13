from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ---------- Schemas ----------
class NoteCreate(BaseModel):
    title: str
    content: str

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str

class Update(BaseModel):
    title: str
    content: str


# ---------- Create Note ----------
@app.post("/notes", status_code=status.HTTP_201_CREATED)
def create(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = models.Notes(**note.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {"Note": new_note}


# ---------- Get Note ----------
@app.get("/notes/{id}")
def get_note(id: int, db: Session = Depends(get_db)):
    note = db.query(models.Notes).filter(models.Notes.id == id).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail=f"Note with id {id} does not exist"
        )

    return {"Note": note}


# ---------- Delete Note ----------
@app.delete("/notes/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    note_query = db.query(models.Notes).filter(models.Notes.id == id)
    note = note_query.first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail=f"Note with id {id} does not exist"
        )

    note_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Note deleted successfully"}


# ---------- Update Note ----------
@app.put("/notes/{id}")
def update(id: int, update: Update, db: Session = Depends(get_db)):
    note_query = db.query(models.Notes).filter(models.Notes.id == id)
    note = note_query.first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail=f"Note with id {id} does not exist"
        )

    note_query.update(update.dict(), synchronize_session=False)
    db.commit()
    db.refresh(note)

    return {"Updated_note": note}