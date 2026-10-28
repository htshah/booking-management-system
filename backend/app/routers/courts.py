from datetime import date as date_type
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/courts", tags=["courts"])

# Simplified fixed operating window used to generate bookable slots for any
# court, regardless of its own `hours_of_operation` text. Good enough for
# this learning project; a real system would parse per-court hours.
SLOT_START_HOUR = 6
SLOT_END_HOUR = 22
SLOT_DURATION_HOURS = 1


@router.get("", response_model=list[schemas.CourtOut])
def list_courts(db: Session = Depends(get_db)):
    return db.query(models.Court).all()


@router.get("/{court_id}", response_model=schemas.CourtOut)
def get_court(court_id: int, db: Session = Depends(get_db)):
    court = db.query(models.Court).filter(models.Court.id == court_id).first()
    if not court:
        raise HTTPException(status_code=404, detail="Court not found")
    return court


@router.get("/{court_id}/availability", response_model=list[schemas.SlotOut])
def get_availability(court_id: int, date: date_type, db: Session = Depends(get_db)):
    court = db.query(models.Court).filter(models.Court.id == court_id).first()
    if not court:
        raise HTTPException(status_code=404, detail="Court not found")

    existing_bookings = (
        db.query(models.Booking)
        .filter(models.Booking.court_id == court_id)
        .all()
    )
    booked_start_times = {
        b.start_timestamp
        for b in existing_bookings
        if b.start_timestamp.date() == date
    }

    slots = []
    for hour in range(SLOT_START_HOUR, SLOT_END_HOUR, SLOT_DURATION_HOURS):
        start = datetime.combine(date, datetime.min.time()) + timedelta(hours=hour)
        end = start + timedelta(hours=SLOT_DURATION_HOURS)
        slots.append(
            {
                "start_timestamp": start,
                "end_timestamp": end,
                "available": start not in booked_start_times,
            }
        )
    return slots
