import sys
import os
from dotenv import load_dotenv
from datetime import date
from fastapi import HTTPException

import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv()

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactUpdate
from src.repository.contacts import (
    create_contact,
    read_contacts,
    find_contact,
    delete_contact,
    update_contact,
    get_future_birthdays,
)

class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_read_contacts_all(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await read_contacts(user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_read_contacts_with_query(self):
        query = "John"
        contacts = [
            Contact(first_name="John", last_name="Kennedy"),
            Contact(first_name="John", last_name="Lewis"),
            Contact(first_name="John", last_name="Smith"),
        ]
        self.session.query().filter().all.return_value = contacts
        result = await read_contacts(q=query, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_find_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await find_contact(contact_id=1, user = self.user, db = self.session)
        self.assertEqual(result, contact)

    async def test_find_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        with self.assertRaises(HTTPException) as context: 
            await find_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(context.exception.status_code, 404)

    async def test_create_contact(self):
        new_contact = ContactModel(first_name = "John",
                            last_name = "Smith",
                            email = "j.smith@yahoo.com",
                            phone = "+38 050 111 22 33",
                            birthday = date.today(),
                            notes = "Test note",)
        result_contact = await create_contact(
            contact=new_contact, user=self.user, db=self.session
        )
        self.assertIsInstance(result_contact, Contact)
        self.assertEqual(new_contact.first_name, result_contact.first_name)
        self.assertEqual(new_contact.last_name, result_contact.last_name)
        self.assertEqual(new_contact.email, result_contact.email)
        self.assertEqual(new_contact.phone, result_contact.phone)
        self.assertEqual(new_contact.birthday, result_contact.birthday)
        self.assertEqual(new_contact.notes, result_contact.notes)
        self.assertTrue(hasattr(result_contact, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await delete_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, {"message": "Contact successfully deleted"})

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        with self.assertRaises(HTTPException) as context:
            await delete_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(context.exception.status_code, 404)

    async def test_update_contact(self):
        contact_body = ContactUpdate(
            first_name="New Name",
            last_name="New Last Name",
            email="new_email@example.com",
            phone="+4915122233344",
            birthday= date.today(),
            notes="New note",
        )
        self.session.query().filter().first.return_value = Contact()
        result_contact = await update_contact(
            contact_id=1,
            user=self.user,
            contact=contact_body,
            db=self.session,
        )
        self.assertIsInstance(result_contact, Contact)


    async def test_update_contact_not_found(self):
        contact_body = ContactUpdate(
            first_name="New Name",
            last_name="New Last Name",
            email="new_email@example.com",
            phone="+4915122233344",
            birthday=date.today(),
            notes="New note",
        )
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        with self.assertRaises(HTTPException) as context: 
            await update_contact(
            contact_id=1,
            user=self.user,
            contact=contact_body,
            db=self.session,
        )
        self.assertEqual(context.exception.status_code, 404)

    async def test_get_future_birthdays(self):
        future_birthday_contacts = [Contact(), Contact()]
        self.session.query().filter().all.return_value = future_birthday_contacts

        future_birthdays = await get_future_birthdays(user=self.user, db=self.session)
        self.assertEqual(future_birthdays, future_birthday_contacts)


if __name__ == "__main__":
    unittest.main()
