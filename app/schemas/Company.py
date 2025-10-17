from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime
from app.schemas.PyObjectId import PyObjectId

class CreateCompanySchema(BaseModel):
    jurisdiction: Optional[str] = Field(None, max_length=100)
    companyName: Optional[str] = Field(None, max_length=200)
    companyAddress: Optional[str] = Field(None, max_length=500)
    zip: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    directors: Optional[str] = Field(None, max_length=1000)
    shareholders: Optional[str] = Field(None, max_length=1000)
    companyActivities: Optional[str] = Field(None, max_length=1000)
    secCode: Optional[str] = Field(None, max_length=50)

class UpdateCompanySchema(BaseModel):
    jurisdiction: Optional[str] = Field(None, max_length=100)
    companyName: Optional[str] = Field(None, max_length=200)
    companyAddress: Optional[str] = Field(None, max_length=500)
    zip: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    directors: Optional[str] = Field(None, max_length=1000)
    shareholders: Optional[str] = Field(None, max_length=1000)
    companyActivities: Optional[str] = Field(None, max_length=1000)
    secCode: Optional[str] = Field(None, max_length=50)

class CompanySchema(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=ObjectId, alias="_id")
    jurisdiction: Optional[str] = Field(None, max_length=100)
    companyName: Optional[str] = Field(None, max_length=200)
    companyAddress: Optional[str] = Field(None, max_length=500)
    zip: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    directors: Optional[str] = Field(None, max_length=1000)
    shareholders: Optional[str] = Field(None, max_length=1000)
    companyActivities: Optional[str] = Field(None, max_length=1000)
    secCode: Optional[str] = Field(None, max_length=50)
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: Optional[datetime] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
