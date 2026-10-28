from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CourtOut(BaseModel):
    id: int
    name: str
    type: str
    address_1: str
    address_2: Optional[str] = None
    city: str
    state: str
    zipcode: str
    image: Optional[str] = None
    hours_of_operation: Optional[str] = None

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    user_id: str
    court_id: int
    start_timestamp: datetime
    end_timestamp: datetime


class BookingOut(BaseModel):
    id: int
    user_id: str
    court_id: int
    start_timestamp: datetime
    end_timestamp: datetime
    court: CourtOut

    class Config:
        from_attributes = True
