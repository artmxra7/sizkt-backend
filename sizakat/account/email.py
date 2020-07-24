from django.core.mail import send_mail
from django.conf import settings


def send_reset_password_token(receiver_email, url, user_id, token):
    subject = 'Reset password akun sizakat'
    reset_password_url = '{}?userId={}&token={}'.format(
        url,
        user_id,
        token
    )
    message = '{}\n{}'.format(
        'Silahkan buka link berikut untuk mengganti password:',
        reset_password_url
    )
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [receiver_email]
    send_mail(subject, message, email_from, recipient_list)
