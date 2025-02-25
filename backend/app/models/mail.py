from fastapi_mail import FastMail, ConnectionConfig # type: ignore
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

conf= ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM = os.getenv("MAIL_USERNAME"),
    MAIL_PORT = 587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,   
    MAIL_SSL_TLS=False,   
    USE_CREDENTIALS=True

)
