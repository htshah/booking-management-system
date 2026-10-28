from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("", response_model=list[schemas.BookingOut])
def list_bookings(user_id: str, db: Session = Depends(get_db)):
    return (
        db.query(models.Booking)
        .filter(models.Booking.user_id == user_id)
        .order_by(models.Booking.start_timestamp.desc())
        .all()
    )


@router.post("", response_model=schemas.BookingOut)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    court = db.query(models.Court).filter(models.Court.id == booking.court_id).first()
    if not court:
        raise HTTPException(status_code=404, detail="Court not found")

    conflict = (
        db.query(models.Booking)
        .filter(
            models.Booking.court_id == booking.court_id,
            models.Booking.start_timestamp == booking.start_timestamp,
        )
        .first()
    )
    if conflict:
        raise HTTPException(status_code=409, detail="That slot is already booked")

    new_booking = models.Booking(**booking.model_dump())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking
