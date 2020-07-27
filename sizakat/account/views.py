import json

from django.http import JsonResponse
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.sessions.models import Session
from django.utils import timezone

from .email import send_reset_password_token

UserModel = get_user_model()


def login_session(request):
    if request.method == 'POST':
        request_body = json.loads(request.body.decode('utf-8'))
        username = request_body.get('username', None)
        password = request_body.get('password', None)
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            session = request.session.session_key
            return JsonResponse({'loggedIn': True, 'session': session})

    return JsonResponse({'loggedIn': False})


def logout_session(request):
    session_key = request.headers.get('Authorization', None)
    session = Session.objects.filter(session_key=session_key)
    if session.exists():
        session.get().delete()
    return JsonResponse({'loggedOut': True})


def reset_password(request):
    if request.method == 'POST':
        request_body = json.loads(request.body.decode('utf-8'))
        email = request_body.get('email', None)
        change_password_url = request_body.get('changePasswordUrl', None)
        try:
            user = UserModel.objects.get(email=email)
            token = token_generator.make_token(user)
            send_reset_password_token(
                email, change_password_url, user.pk, token)
            return JsonResponse({'success': True})

        except UserModel.DoesNotExist:
            return JsonResponse({'success': False}, status=404)

    return JsonResponse({'success': False}, status=405)


def change_reset_password(request):
    if request.method == 'POST':
        request_body = json.loads(request.body.decode('utf-8'))
        user_id = request_body.get('userId', None)
        token = request_body.get('token', None)
        try:
            user = UserModel.objects.get(pk=user_id)
            if token_generator.check_token(user, token):
                new_pass = request_body.get('newPassword')
                user.set_password(new_pass)
                user.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False}, status=401)

        except UserModel.DoesNotExist:
            return JsonResponse({'success': False}, status=404)

    return JsonResponse({'success': False}, status=405)


def verify_session(request):
    session_key = request.headers.get('Authorization', None)
    session = Session.objects.filter(session_key=session_key)
    if session.exists():
        expire_time = session.get().expire_date
        if timezone.now() < expire_time:
            return JsonResponse({'active': True})
        else:
            session.get().delete()
    return JsonResponse({'active': False})
