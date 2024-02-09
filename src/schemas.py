from pydantic import BaseModel, EmailStr
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
    notes: str = None


    class Config:
        orm_mode = True
