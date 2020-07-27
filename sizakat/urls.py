"""sizakat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from .account.views import change_reset_password, login_session, logout_session, reset_password, verify_session

urlpatterns = [
    path('admin/', admin.site.urls),

    # login path for form login
    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),

    path('login/', csrf_exempt(login_session)),
    path('logout/', csrf_exempt(logout_session)),
    path('reset-password/', csrf_exempt(reset_password)),
    path('change-reset-password/', csrf_exempt(change_reset_password)),
    path('verify-session/', verify_session),
]
