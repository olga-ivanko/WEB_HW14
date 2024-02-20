from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber
from datetime import datetime, date

class ContactModel(BaseModel):
    first_name: str = None
    last_name: str = None
    email: EmailStr = None
    phone: PhoneNumber = "+38 123 456 78 99"
    birthday: date = None
    notes: str = None


class ContactUpdate(ContactModel):
    pass


class ContactResponse(ContactModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: PhoneNumber
    birthday: date 
    notes: str

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    username: str = Field(min_lengs = 5, max_length = 16)
    email: EmailStr = None
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
