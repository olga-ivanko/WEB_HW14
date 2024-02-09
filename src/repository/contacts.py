from fastapi import Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, extract
from src.database.models import Contact
from src.database.db import get_db
from src.schemas import ContactModel, ContactUpdate, ContactResponse
from datetime import datetime, timedelta


async def create_contact(contact: ContactModel, db: Session = Depends(get_db)):
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


async def read_contacts(db: Session = Depends(get_db), q: str = None):
    if q:
        return (
            db.query(Contact)
            .filter(
                or_(
                    Contact.first_name.ilike(f"%{q}%"),
                    Contact.last_name.ilike(f"%{q}%"),
                    Contact.email.ilike(f"%{q}%"),
                )
            )
            .all()
        )
    return db.query(Contact).all()


async def find_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(
            status_code=404, detail=f"Contact with id: {contact_id} was not found"
        )
    return db_contact


async def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    
    if db_contact is None:
        raise HTTPException(
            status_code=404, detail=f"Contact with id: {contact_id} was not found"
        )

    if contact.first_name != db_contact.first_name and contact.first_name != "string":
        db_contact.first_name = contact.first_name

    if contact.last_name != db_contact.last_name and contact.last_name != "string":
        db_contact.last_name = contact.last_name

    if contact.email != db_contact.email and contact.email != "user@example.com":
        db_contact.email = contact.email

    if contact.phone != db_contact.phone and contact.phone != "tel:+381-23-4567899":
        db_contact.phone = contact.phone

    if contact.birthday != db_contact.birthday and contact.birthday != datetime.today():
        db_contact.birthday = contact.birthday

    if contact.notes != db_contact.notes and contact.notes != "string":
        db_contact.notes = contact.notes

    db.commit()
    db.refresh(db_contact)
    return db_contact


async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(
            status_code=404, detail=f"Contact with id: {contact_id} was not found"
        )
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact successfully deleted"}


async def get_future_birthdays(db: Session = Depends(get_db)):
    today = datetime.now().date()
    end_date = today + timedelta(days=7)
   

    result = (
        db.query(Contact)
        .filter(

                or_(
                    and_(
                        extract("month", Contact.birthday) == today.month,
                        extract("day", Contact.birthday) >= today.day,
                        extract("day", Contact.birthday) <= end_date.day
                    ),
                    and_(
                        extract("month", Contact.birthday) == end_date.month,
                        extract("day", Contact.birthday) <= end_date.day
                )
            )
        )
        .all()
    )
    return result
