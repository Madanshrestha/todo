from django.core.mail import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            from_email= os.getenv('EMAIL_FROM'),
            to=[data['to_email']]
        )
        email.send()