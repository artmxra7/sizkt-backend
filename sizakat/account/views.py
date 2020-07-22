import json

from django.http import JsonResponse
from django.contrib.auth import authenticate, login


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

    return JsonResponse({'message': 'login failed'})
