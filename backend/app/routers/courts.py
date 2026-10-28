from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/courts", tags=["courts"])


@router.get("", response_model=list[schemas.CourtOut])
def list_courts(db: Session = Depends(get_db)):
    return db.query(models.Court).all()


@router.get("/{court_id}", response_model=schemas.CourtOut)
def get_court(court_id: int, db: Session = Depends(get_db)):
    court = db.query(models.Court).filter(models.Court.id == court_id).first()
    if not court:
        raise HTTPException(status_code=404, detail="Court not found")
    return court
