from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import bcrypt

from database import get_db
from models import Organization, User, Service
from schemas import StaffCreate, ServiceUpdate, OrganizationUpdate

app = FastAPI()


@app.post("/config/staff")
def create_staff(data: StaffCreate, db: Session = Depends(get_db)):
    """Наем новых сотрудников"""
    org = db.query(Organization).filter(Organization.id == data.org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt())

    staff = User(
        org_id=data.org_id,
        email=data.email,
        password_hash=hashed.decode('utf-8'),
        role=data.role,
        full_name=data.full_name
    )

    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff


@app.put("/config/services")
def create_or_update_service(data: ServiceUpdate, db: Session = Depends(get_db)):
    """Настройка «меню» услуг"""
    org = db.query(Organization).filter(Organization.id == data.org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    service = Service(
        org_id=data.org_id,
        title=data.title,
        description=data.description,
        base_price=data.base_price,
        duration_minutes=data.duration_minutes,
        is_active=data.is_active
    )

    db.add(service)
    db.commit()
    db.refresh(service)
    return service


@app.patch("/config/organization")
def update_organization(data: OrganizationUpdate, db: Session = Depends(get_db)):
    """Смена настроек бизнеса (время работы, логотип, уведомления)"""
    org = db.query(Organization).filter(Organization.id == data.org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    update_data = data.model_dump(exclude_unset=True, exclude={"org_id"})

    for key, value in update_data.items():
        setattr(org, key, value)

    db.commit()
    db.refresh(org)
    return org