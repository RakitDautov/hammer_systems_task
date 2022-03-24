from django.urls import path
from .views import registration_phone, me, get_token, post_invite_code

urlpatterns = [
    path("auth/", get_token, name="token"),
    path("sing_in/", registration_phone, name="registration"),
    path("me/", me, name="get_yourself"),
    path("invite_code/", post_invite_code, name="post_invite_code"),
]
