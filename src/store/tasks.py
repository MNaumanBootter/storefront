from time import sleep
from celery import shared_task
from templated_mail.mail import BaseEmailMessage
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage


@shared_task
def email_customers():
    print('Sending emails...')
    sleep(10)
    try:
        send_mail(
            "subject",
            "message",
            "from@example.com",
            ["user@example.com"],
            html_message="sup",
        )
        mail_admins(
            "subject",
            "message",
            html_message="sup",
        )
        message = EmailMessage(
            "subject", "message", "from@example.com", ["john@example.com"]
        )
        message.attach_file("store/static/store/styles.css")
        message.send()
        template_message = BaseEmailMessage(
            template_name="emails/hello.html",
            context={"name": "Name"},
        )
        template_message.send(["john@example.com"])
    except BadHeaderError:
        print("Bad Header Error")
    print('Emails were successfully sent!')
