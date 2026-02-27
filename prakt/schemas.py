import uuid

from pydantic import BaseModel

class OrganizationCreate(BaseModel):
    name: str
    slug: str

class UserCreate(BaseModel):
    email: str
    password: uuid.UUID
    organization_id: str

class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    email: str
    role: str
    organization_id: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: uuid.UUID
    role: str
    organization_id: str