from fastapi import APIRouter, Depends, status
from src.database.db import get_db
from sqlalchemy.orm import Session
from src.repository import contacts as repository_contacts
from src.schemas import ContactModel, ContactUpdate, ContactResponse
from typing import List

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactResponse)
async def create_contact(contact: ContactModel, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(contact, db)


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(db: Session = Depends(get_db), q: str = None):
    contacts = await repository_contacts.read_contacts(db, q)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.read_contact(contact_id, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)
):
    contact = await repository_contacts.update_contact(contact_id, contact, db)
    return contact


@router.delete("/{contact_id}")
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.delete_contact(contact_id, db)
    return contact


@router.get("/birthdays", response_model=List[ContactResponse])
async def get_future_birthdays(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_future_birthdays(db)
    return contacts
