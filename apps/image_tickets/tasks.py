from celery import shared_task
from django.db import transaction

from apps.image_tickets.repository import CloudinaryRepository
from .models import Ticket, TicketStatus


@shared_task
def upload_image_into_cloud_storage(image_url: str):
    try:
        cloud_provider = CloudinaryRepository()
        cloud_provider.upload_image(image_url)
        print(f"Image uploaded successfully")
    except Exception as e:
        print(f"Image upload failed with error: {e}")
        raise


@shared_task
def update_ticket(_, ticket_id: int):
    try:
        with transaction.atomic():
            ticket = Ticket.objects.select_for_update().get(pk=ticket_id)
            new_loaded_image_quantity = ticket.loaded_image_quantity + 1
            ticket.loaded_image_quantity = new_loaded_image_quantity
            if new_loaded_image_quantity == ticket.max_image_quantity:
                ticket.status = TicketStatus.COMPLETED
            ticket.save()
    except Ticket.DoesNotExist:
        print(f"Ticket with id {ticket_id} does not exist")
    except Exception as e:
        print(f"Ticket update failed with error: {e}")
        raise
