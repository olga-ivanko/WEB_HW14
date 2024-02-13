from fastapi import APIRouter, Depends, status
from src.database.db import get_db
from sqlalchemy.orm import Session
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
from src.schemas import ContactModel, ContactUpdate, ContactResponse
from src.database.models import User
from typing import List

router = APIRouter(prefix="/contacts", tags=["contacts"])
router_b = APIRouter(prefix="/contacts/birthdays", tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact: ContactModel,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await repository_contacts.create_contact(contact, current_user, db)


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    q: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contacts = await repository_contacts.read_contacts(db, q, current_user)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def find_contact(
    contact_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contact = await repository_contacts.find_contact(contact_id, current_user, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user), 
    
):
    contact = await repository_contacts.update_contact(contact_id, current_user, contact, db)
    return contact


@router.delete("/{contact_id}")
async def delete_contact(
    contact_id: int,
    current_user: User = Depends(auth_service.get_current_user), 
    db: Session = Depends(get_db)
):
    contact = await repository_contacts.delete_contact(contact_id, current_user, db)
    return contact


@router_b.get("/", response_model=List[ContactResponse])
async def get_future_birthdays(
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    contacts = await repository_contacts.get_future_birthdays(current_user, db)
    return contacts
