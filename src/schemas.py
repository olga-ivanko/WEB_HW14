from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from datetime import datetime, date

class ContactModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: PhoneNumber
    birthday: date = date.today()
    notes: str = None


class ContactUpdate(ContactModel):
    pass


class ContactResponse(ContactModel):
    id: int

    class Config:
        orm_mode = True
