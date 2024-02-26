from fastapi import APIRouter, Depends, status
from fastapi_limiter.depends import RateLimiter
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
    """
    Create a new contact for the specific user.

    :param contact: The data for the contact to be created.
    :type contact: ContactModel
    :param db: The database session.
    :type db: Session
    :param current_user: The user to create the contact for.
    :type current_user: User
    :return: The newly created contact.
    :rtype: ContactResponse
    """
    return await repository_contacts.create_contact(contact, current_user, db)


@router.get(
    "/",
    response_model=List[ContactResponse],
    description="No more that 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def read_contacts(
    q: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Retrieve all contacts for the specific user, optionally filtered by a search query.

    :param q: The search query. Defaults to None.
    :type q: str
    :param db: The database session.
    :type db: Session
    :param user: The user to retrieve contacts for.
    :type user: User
    :return: List of contacts matching the search query if provided or all contacts of the user, if query is None.
    :rtype: List[Contact]
    """
    contacts = await repository_contacts.read_contacts(db, q, current_user)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def find_contact(
    contact_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Retrieves a single contact with specified ID for the specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The user to retrieve contact for.
    :type current_user: User
    :raises HTTPException: If the contact with the specified ID is not found.
    :return: The found contact.
    """
    contact = await repository_contacts.find_contact(contact_id, current_user, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user), 
    
):
    """
    Update a specified contact's details for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param contact: The updated contact details.
    :type contact: ContactUpdate
    :param db: The database session.
    :type db: Session
    :param current_user: The user to whom the contact belongs.
    :type current_user: User
    :raises HTTPException: If the contact with the specified ID is not found.
    :return: The updated contact.
    :rtype: ContactResponse
    """
    contact = await repository_contacts.update_contact(contact_id, current_user, contact, db)
    return contact


@router.delete("/{contact_id}")
async def delete_contact(
    contact_id: int,
    current_user: User = Depends(auth_service.get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to delete.
    :type contact_id: int
    :param current_user: The user to remove the contact for.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :raises HTTPException: If the contact with the specified ID is not found.
    :return: A message confirming the deletion.
    :rtype: dict
    """
    contact = await repository_contacts.delete_contact(contact_id, current_user, db)
    return contact


@router_b.get("/", response_model=List[ContactResponse])
async def get_future_birthdays(
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all contacts with birthdays within next 7 days for a specific user.

    :param current_user: The user to retrieve the contacts for.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: Contacts with birthdays within next 7 days.
    :rtype: List[ContactResponse]
    """
    contacts = await repository_contacts.get_future_birthdays(current_user, db)
    return contacts
