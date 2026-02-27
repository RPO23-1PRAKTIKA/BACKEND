from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import Organization, User
from schemas import OrganizationCreate, UserCreate, UserResponse, Token, TokenData
from database import SessionLocal
from jose import JWTError, jwt
from datetime import timedelta
import datetime
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/auth/register", response_model=UserResponse)
def register_user(org: OrganizationCreate, user: UserCreate, db: Session = Depends(get_db)):

    organization = Organization(**org.model_dump())
    db.add(organization)
    db.commit()
    db.refresh(organization)


    hashed_password = pwd_context.hash(str(user.password))
    db_user = User(email=user.email, hashed_password=hashed_password,
                   organization_id=organization.id)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post("/auth/token", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not pwd_context.verify(str(user.password), str(db_user.hashed_password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password",
                            headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"id": db_user.id,
                                             "role": db_user.role,
                                             "organization_id": db_user.organization_id},
                                       expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/auth/me", response_model=TokenData)
def read_users_me(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: UUID = UUID(str(payload.get("id")))
        if user_id is None:
            raise credentials_exception
        TokenData(
            id=user_id,
            role=payload.get("role"),
            organization_id=payload.get("organization_id")
        )

    except JWTError:
        raise credentials_exception
    except ValueError:
        raise credentials_exception