from re import sub
import smtplib
import os

EMAIL_USER = os.environ.get("FAAUTH_EMAIL")
EMAIL_PASS = os.environ.get("FAAUTH_PASS")
EMAIL_FROM = os.environ.get("FAAUTH_FROM")
EMAIL_SMTP = os.environ.get("FAAUTH_SMTP")


def send_invitation_email(to: str, first_name: str, registration_link: str):
    message_body = f"""
        Greetings {first_name}, welcome to our app!\n\n\n
        In order to complete your registration please click on the following link:\n
        {registration_link}\n\n
        Thank you,\n
        FastAPI Auth Template Team
    """
    send_email(to, "Confirm your email address", message_body)


def send_email(to: str, subject: str, body: str):
    message = create_message(to, subject, body)
    try:
        print(f"{EMAIL_FROM} {EMAIL_PASS} {EMAIL_SMTP} {EMAIL_USER}")
        server_ssl = smtplib.SMTP_SSL(EMAIL_SMTP, 465)
        server_ssl.ehlo()
        server_ssl.login(EMAIL_USER, EMAIL_PASS)
        server_ssl.sendmail(EMAIL_FROM, to, message)
        server_ssl.close()
    except Exception as ex:
        print(ex)


def create_message(to: str, subject: str, body: str):
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (
        EMAIL_FROM,
        ", ".join(to),
        subject,
        body,
    )

    return message
