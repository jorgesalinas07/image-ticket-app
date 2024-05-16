from django.urls import path
from apps.users import views

urlpatterns = [
    path('', views.home, name='home')
]
