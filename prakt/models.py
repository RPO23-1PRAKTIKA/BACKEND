from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    timezone = Column(String, default='Europe/Moscow')
    created_at = Column(TIMESTAMP, nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default='owner')  # owner, manager, employee
    organization_id = Column(str(ForeignKey("organizations.id")), nullable=False)
    is_active = Column(Boolean, default=True)

    organization = relationship("Organization")