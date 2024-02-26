import os
from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.services.auth import auth_service
from src.conf.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.email_username,
    MAIL_PASSWORD=settings.email_password,
    MAIL_FROM=settings.email_from,
    MAIL_PORT=settings.email_port,
    MAIL_SERVER=settings.email_server,
    MAIL_FROM_NAME="Rest API Application",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / "templates",
)


async def send_email(email: EmailStr, username: str, host: str):
    """
    Send an email for email verification.

    :param email: The user's email address.
    :type email: EmailStr
    :param username: The username of the user.
    :type username: str
    :param host: The host URL for the application.
    :type host: str
    """
    try: 
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject = "Confirm your email", 
            recipients=[email], 
            template_body={"host": host, 
                           "username": username, 
                           "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as err: 
        print(err)
