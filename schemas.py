from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from uuid import UUID
from datetime import time
import enum


class UserRole(str, enum.Enum):
    owner = "owner"
    staff = "staff"
    customer = "customer"


class StaffCreate(BaseModel):
    org_id: UUID
    email: str
    password: str
    full_name: str
    role: UserRole = UserRole.staff


class ServiceUpdate(BaseModel):
    org_id: UUID
    title: str
    description: Optional[str] = None
    base_price: Decimal
    duration_minutes: int = 60
    is_active: bool = True


class OrganizationUpdate(BaseModel):
    org_id: UUID
    working_hours_start: Optional[time] = None
    working_hours_end: Optional[time] = None
    logo_url: Optional[str] = None
    notifications_enabled: Optional[bool] = None