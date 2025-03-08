"""
Ce module contient des services pour l'envoi d'emails via FastAPI Mail.
"""

from fastapi_mail import FastMail, MessageSchema

from backend.app.models.mail import conf

fm = FastMail(conf)

async def send_verification_email(email: str, username: str):
    """
    Envoie un email de vérification à l'utilisateur après son inscription.

    Args:
        email (str): L'adresse email de l'utilisateur.
        username (str): Le nom d'utilisateur de l'utilisateur.

    Returns:
        None: La fonction envoie un email mais ne retourne rien.

    Utilise FastMail pour envoyer un email contenant un lien de vérification.
    """
    verification_link = f"http://localhost:8000/verify-email/{username}"
    message = MessageSchema(
        subject="Vérification de votre compte",
        recipients=[email],
        body=f"""
        Bonjour {username},

        Merci de vous être inscrit sur notre plateforme !
        Veuillez cliquer sur le lien suivant pour vérifier votre adresse e-mail :

        {verification_link} (le lien ne marche pas mais l'idée est là)

        Cordialement,
        L'équipe de support.
        """,
        subtype="plain"
    )
    await fm.send_message(message)
