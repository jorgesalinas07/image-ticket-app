from django.urls import path
from apps.users import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("test_token/", views.test_token, name="test_token"),
]
