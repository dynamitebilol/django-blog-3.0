from django.urls import path
from .views_api import LoginView, RegisterView

urlpatterns = [
    path('login/', LoginView),
    path('register/', RegisterView),
]