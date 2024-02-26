from fastapi import Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, extract
from src.database.models import Contact, User
from src.schemas import ContactModel, ContactUpdate
from datetime import datetime, timedelta


async def create_contact(contact: ContactModel, user: User, db: Session):
    """
    Create a new contact for the specific user.

    :param contact: The data for the contact to be created.
    :type contact: ContactModel
    :param user: The user to create the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
    db_contact = Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone=contact.phone,
        birthday=contact.birthday,
        notes=contact.notes,
        user=user,
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


async def read_contacts(db: Session, q: str = None, user = User):
    """
    Retrieve all contacts for the specific user, optionally filtered by a search query.

    :param db: The database session.
    :type db: Session
    :param q: The search query. Defaults to None.
    :type q: str
    :param user: The user to retrieve contacts for.
    :type user: User
    :return: List of contacts matching the search query if provided or all contacts of the user, if query is None.
    :rtype: List[Contact]
    """
    if q:
        return (
            db.query(Contact)
            .filter(
                and_(
                    or_(
                        Contact.first_name.ilike(f"%{q}%"),
                        Contact.last_name.ilike(f"%{q}%"),
                        Contact.email.ilike(f"%{q}%"),
                    ),
                    Contact.user_id == user.id,
                )
            )
            .all()
        )

    return db.query(Contact).filter(Contact.user_id == user.id).all()


async def find_contact(contact_id: int, user: User, db: Session):
    """
    Retrieves a single contact with specified ID for the specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :raises HTTPException: If the contact with the specified ID is not found.
    :return: The found contact.
    :rtype: Contact
    """
    db_contact = (
        db.query(Contact)
        .filter(and_(Contact.user_id == user.id, Contact.id == contact_id))
        .first()
    )
    if db_contact is None:
        raise HTTPException(
            status_code=404, detail=f"Contact with id: {contact_id} was not found"
        )
    return db_contact


async def update_contact(
    contact_id: int, user: User, contact: ContactUpdate, db: Session
):
    """
    Update a specified contact's details for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param user: The user to whom the contact belongs.
    :type user: User
    :param contact: The updated contact details.
    :type contact: ContactUpdate
    :param db: The database session.
    :type db: Session
    :raises HTTPException: If the contact with the specified ID is not found.
    :return: The updated contact.
    :rtype: Contact
    """
    db_contact = (
        db.query(Contact)
        .filter(and_(Contact.user_id == user.id, Contact.id == contact_id))
        .first()
    )

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


async def delete_contact(contact_id: int, user: User, db: Session):
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to delete.
    :type contact_id: int
    :param user: The user to remove the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :raises HTTPException: If the contact with the specified ID is not found.
    :return: A message confirming the deletion.
    :rtype: dict
    """
    db_contact = (
        db.query(Contact)
        .filter(and_(Contact.user_id == user.id, Contact.id == contact_id))
        .first()
    )
    if db_contact is None:
        raise HTTPException(
            status_code=404, detail=f"Contact with id: {contact_id} was not found"
        )
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact successfully deleted"}


async def get_future_birthdays(user: User, db: Session):
    """
    Retrieve all contacts with birthdays within next 7 days for a specific user.

    :param user: The user to retrieve the contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: Contacts with birthdays within next 7 days.
    :rtype: List[Contact]
    """
    today = datetime.now().date()
    end_date = today + timedelta(days=7)

    result = (
        db.query(Contact)
        .filter(
            or_(
                and_(
                    extract("month", Contact.birthday) == today.month,
                    extract("day", Contact.birthday) >= today.day,
                    extract("day", Contact.birthday) <= end_date.day,
                    Contact.user_id == user.id,
                ),
                and_(
                    extract("month", Contact.birthday) == end_date.month,
                    extract("day", Contact.birthday) <= end_date.day,
                    Contact.user_id == user.id,
                ),
            )
        )
        .all()
    )
    return result
