from django.urls import path
from rest_framework.authtoken import views
from .views import UserAPIView, HuntingAPIView, CustomAuthToken, WelcomeAPIView

urlpatterns = [
    path('users/<int:id>/', UserAPIView.as_view()),
    path('hunting/<int:idcat>/', HuntingAPIView.as_view()),
    path('login/', CustomAuthToken.as_view()),
    path('', WelcomeAPIView.as_view())
]
