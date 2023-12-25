from django.core.mail import send_mail
from decouple import config


def send_approval_email(user_email, date, type):
    subject = 'Solicitação Aprovada'
    message = f'Sua solicitação de {type} para o dia {
        date} foi aprovada. Entre em contato para mais informações.'
    from_email = config("EMAIL_HOST_USER")
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)


def send_rejection_email(user_email, date, type):
    subject = 'Solicitação Reprovada'
    message = f'Sua solicitação de {type} para o dia {
        date} foi reprovada. Entre em contato para mais informações.'
    from_email = config("EMAIL_HOST_USER")

    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
