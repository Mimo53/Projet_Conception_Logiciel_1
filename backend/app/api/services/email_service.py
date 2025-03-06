from fastapi_mail import FastMail, MessageSchema

from backend.app.models.mail import conf

fm = FastMail(conf)

async def send_verification_email(email: str, username: str):
    verification_link = f"http://localhost:8000/verify-email/{username}"
    message = MessageSchema(
        subject="Vérification de votre compte",
        recipients=[email],
        body=f"""
        Bonjour {username},

        Merci de vous être inscrit sur notre plateforme !
        Veuillez cliquer sur le lien suivant pour vérifier votre adresse e-mail :

        {verification_link}

        Cordialement,
        L'équipe de support.
        """,
        subtype="plain"
    )
    await fm.send_message(message)
