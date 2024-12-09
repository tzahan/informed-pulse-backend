from pydantic import BaseModel, EmailStr, Field
from datetime import date

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    preferences: list[str] = Field(..., description="List of user preferences")
    date_of_birth: date = Field(..., description="Date of birth in YYYY-MM-DD format")
    """
    name: str
    email: EmailStr
    password: str
    date_of_birth: date
    preferences: list[str]
    """

class LoginRequest(BaseModel):
    email: str
    password: str

class PreferencesUpdate(BaseModel):
    preferences: list[str]

class InteractionRequest(BaseModel):
    news_id: str


