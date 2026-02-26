from datetime import datetime, time, date
from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel


# ========== EXISTING SCHEMAS ==========

class StaffCreate(BaseModel):
    org_id: UUID
    email: str
    password: str
    full_name: str
    role: str = "staff"


class ServiceUpdate(BaseModel):
    org_id: UUID
    title: str
    description: Optional[str] = None
    base_price: Decimal
    duration_minutes: int = 60
    is_active: bool = True


class OrganizationUpdate(BaseModel):
    org_id: UUID
    name: Optional[str] = None
    working_hours_start: Optional[time] = None
    working_hours_end: Optional[time] = None
    logo_url: Optional[str] = None
    notifications_enabled: Optional[bool] = None


# ========== CLIENT BOOKING SCHEMAS ==========

class StaffResponse(BaseModel):
    id: UUID
    full_name: str
    email: str
    role: str

    class Config:
        from_attributes = True


class TimeSlot(BaseModel):
    start: str
    end: str


class FreeSlotsResponse(BaseModel):
    org_id: UUID
    staff_id: UUID
    staff_name: str
    date: str
    working_hours_start: time
    working_hours_end: time
    slots: List[TimeSlot]


class BookingCreate(BaseModel):
    org_id: UUID
    staff_id: UUID
    service_id: UUID
    customer_id: UUID
    start_at: datetime


class BookingResponse(BaseModel):
    id: UUID
    org_id: UUID
    staff_id: UUID
    service_id: UUID
    customer_id: UUID
    start_at: datetime
    end_at: datetime
    status: str

    class Config:
        from_attributes = True


class MyBookingResponse(BaseModel):
    id: UUID
    org_name: Optional[str]
    staff_name: Optional[str]
    service_title: Optional[str]
    start_at: datetime
    end_at: datetime
    status: str
    price: Optional[Decimal]