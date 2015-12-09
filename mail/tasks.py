from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_mail(mail):
    """
    Send an email.

    :param mail: Email to send
    :type mail: EmailMessage
    """
    if not isinstance(mail, EmailMessage):
        raise ValueError("Mail argument must be an instance of django.core.mail.EmailMessage")

    mail.send()
