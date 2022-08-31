from django.urls import path
from users.views import signup_post, token_post

urlpatterns = [
    path('v1/auth/token/', token_post),
    path('v1/auth/signup/', signup_post),
]
