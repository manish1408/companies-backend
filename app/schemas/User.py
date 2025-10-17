from pydantic import BaseModel, Field, EmailStr, constr
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
from enum import Enum
from app.schemas.PyObjectId import PyObjectId

class UserType(str, Enum):
    ADMIN = "admin"
    USER = "user"

class CreateUserSchema(BaseModel):
    fullName: str = Field(..., min_length=2, max_length=50)
    email: EmailStr = Field(...)
    phone: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')
    password: str = Field(..., min_length=8)
    userType: UserType = Field(default=UserType.USER)

class AdminCreateUserSchema(BaseModel):
    fullName: str = Field(..., min_length=2, max_length=50)
    email: EmailStr = Field(...)
    phone: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')
    password: str = Field(..., min_length=8)

class UpdateUserSchema(BaseModel):
    email: Optional[EmailStr] = None
    fullName: Optional[str] = Field(None, min_length=2, max_length=50)
    address: Optional[str] = Field(None, max_length=200)
    city: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    zip: Optional[str] = Field(None)
    profilePicture: Optional[str] = None
    phone: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')

class AdminUpdateUserSchema(BaseModel):
    email: Optional[EmailStr] = None
    fullName: Optional[str] = Field(None, min_length=2, max_length=50)
    phone: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')
    userType: Optional[UserType] = None

class UserSchema(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=ObjectId, alias="_id")
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)
    fullName: str = Field(..., min_length=2, max_length=50)
    userType: UserType = Field(default=UserType.USER)
    address: Optional[str] = Field(None, max_length=200)
    city: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    zip: Optional[str] = Field(None)
    profilePicture: Optional[str] = None
    phone: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')
    adminId: Optional[str] = None  
    createdOn: datetime = Field(default_factory=datetime.utcnow)
    updatedOn: Optional[datetime] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

#Get user Schema 
class GetUserSchema(BaseModel):
    email: EmailStr
    password: str



    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        
    
    