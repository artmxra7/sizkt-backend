import json

from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.tokens import default_token_generator as token_generator

from .email import send_reset_password_token

UserModel = get_user_model()


def post_login(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body.get('username', '')
        password = body.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'login succeeded'})
        else:
            return JsonResponse({'message': 'login failed'}, status=401)

    return JsonResponse({'message': 'method not allowed'}, status=405)


def post_logout(request):
    logout(request)
    return JsonResponse({'message': 'logout succeeded'})


def reset_password(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        email = body.get('email', '')
        change_password_url = body.get('changePasswordUrl', '')
        try:
            user = UserModel.objects.get(email=email)
            token = token_generator.make_token(user)
            send_reset_password_token(
                email, change_password_url, user.pk, token)
            return JsonResponse({'message': 'reset token has been sent to your email'})

        except UserModel.DoesNotExist:
            return JsonResponse({'message': 'user not found'}, status=404)

    return JsonResponse({'message': 'method not allowed'}, status=405)


def change_reset_password(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        user_id = body.get('userId', 0)
        token = body.get('token', '')
        try:
            user = UserModel.objects.get(pk=user_id)
            if token_generator.check_token(user, token):
                new_pass = body.get('newPassword')
                user.set_password(new_pass)
                user.save()
                return JsonResponse({'message': 'password successfully changed'})
            else:
                return JsonResponse({'message': 'invalid reset token: unauthorized'}, status=401)
            return JsonResponse({'userId': user.pk, 'token': token})

        except UserModel.DoesNotExist:
            return JsonResponse({'message': 'user not found'}, status=404)

    return JsonResponse({'message': 'method not allowed'}, status=405)
