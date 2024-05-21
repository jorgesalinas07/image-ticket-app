from django.urls import path
from . import views

urlpatterns = [
    path("", views.ticket_view, name="create or get tickets"),
    path(
        "<int:pk>/", views.get_by_id, name="get a ticket by id"
    ),  ## Check how to remove initial / to eliminate warning
    path("<int:pk>/image", views.upload_image, name="upload image a to ticket by id"),
]
