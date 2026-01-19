import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def send_email(
    subject: str,
    html_body: str,
    sender_email: str,
    sender_password: str,
    recipient_email: str,
    smtp_server: str,
    smtp_port: int,
):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg.set_content("Ce mail nécessite un affichage HTML.")
    msg.add_alternative(html_body, subtype="html")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("Email envoyé avec succès.")
    except Exception as e:
        print(f"Échec de l'envoi du mail : {e}")


def send_formatted_mail(receiver: str, name: str):
    subject = "[Aurianne Léo] - Nouveau message reçu sur le site"
    html_body = f"""
    <html>
    <head>
        <style>
            body {{
                background-color: #fff4ec;
                font-family: 'Comic Sans MS', cursive, sans-serif;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                background-color: #fff9f5;
                border-radius: 16px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.05);
                max-width: 600px;
                margin: auto;
                padding: 30px;
                border: 2px dashed #fcd5ce;
            }}
            .title {{
                color: #b08968;
                font-size: 28px;
                margin-bottom: 15px;
            }}
            .message {{
                color: #7f5539;
                font-size: 18px;
                margin-bottom: 30px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 20px;
                background-color: #ffc8dd;
                color: #6d6875;
                text-decoration: none;
                font-weight: bold;
                border-radius: 25px;
                border: 2px solid #ffafcc;
                transition: background-color 0.3s;
            }}
            .button:hover {{
                background-color: #ffafcc;
            }}
            .footer {{
                margin-top: 40px;
                font-size: 14px;
                color: #a49191;
                text-align: center;
            }}
            img.logo {{
                display: block;
                margin: 0 auto 20px;
                width: 100px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <img src="https://i.imgur.com/wUG8pS5.mp4" class="logo" alt="Cute Logo">
            <div class="title">Bonjour {name} 🧸🐐</div>
            <div class="message">
                Tu as reçu un nouveau message tout doux sur ton site !
            </div>
            <a class="button" href="https://al.lchappuis.fr">Voir le message</a>
            <div class="footer">
                Je t'aime 💌<br/>
                 🌷
            </div>
        </div>
    </body>
    </html>    
    """

    sender_email = os.getenv("MAIL_USERNAME")
    sender_password = os.getenv("MAIL_PASSWORD")
    smtp_server = os.getenv("MAIL_HOST")
    smtp_port = int(os.getenv("MAIL_PORT", 587))  # Port par défaut si non défini

    send_email(
        subject,
        html_body,
        sender_email,
        sender_password,
        receiver,
        smtp_server,
        smtp_port,
    )
