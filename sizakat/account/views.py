from django.shortcuts import redirect
from django.conf import settings


def reset_password(request):
    token = request.GET.get('token', '')
    reset_password_url = settings.RESET_PASSWORD_URL
    return redirect(f'{reset_password_url}?token={token}')
