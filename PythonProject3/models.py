from sqlalchemy import (
    Column, String, Integer, ForeignKey, DateTime,
    Enum, Boolean, Time, Numeric, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from database import Base


# Enums
class UserRole(str, enum.Enum):
    owner = "owner"
    manager = "manager"
    staff = "staff"
    customer = "customer"


class AppointmentStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"


class TimeOffType(str, enum.Enum):
    vacation = "vacation"
    sick_leave = "sick_leave"
    break_time = "break_time"


# Models
class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(50), nullable=False, unique=True)
    timezone = Column(String(50), default="Europe/Moscow")
    working_hours_start = Column(Time)
    working_hours_end = Column(Time)
    logo_url = Column(Text)
    notifications_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=False), server_default=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="staff")
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=False), server_default=func.now())


class Service(Base):
    __tablename__ = "services"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    base_price = Column(Numeric(10, 2), nullable=False)
    duration_minutes = Column(Integer, default=60)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=False), server_default=func.now())


class StaffService(Base):
    __tablename__ = "staff_services"

    staff_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"), primary_key=True)
    price = Column(Numeric(10, 2))
    duration_minutes = Column(Integer)


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    staff_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=False)
    start_at = Column(DateTime(timezone=False), nullable=False)
    end_at = Column(DateTime(timezone=False), nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.pending)


class TimeOff(Base):
    __tablename__ = "time_off"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    start_at = Column(DateTime(timezone=False))
    end_at = Column(DateTime(timezone=False))
    type = Column(Enum(TimeOffType))


class WorkingHours(Base):
    __tablename__ = "working_hours"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    day_of_week = Column(Integer)  # 1=Monday, 7=Sunday
    start_time = Column(Time)
    end_time = Column(Time)