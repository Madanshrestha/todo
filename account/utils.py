from django.core.mail import EmailMessage
import environ

env = environ.Env()

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            from_email= env('EMAIL_FROM'),
            to=[data['to_email']]
        )
        email.send()