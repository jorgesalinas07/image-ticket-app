from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_ticket, name='create a ticket'),
]
