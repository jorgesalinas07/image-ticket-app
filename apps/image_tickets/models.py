from django.utils import timezone
from django.db import models

class TicketStatus(models.TextChoices):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'

class Ticket(models.Model):
    status = models.CharField(
        max_length=100,
        choices=TicketStatus.choices,
        default=TicketStatus.PENDING,
    )
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        blank=False,
    )
    created_at = models.DateTimeField(
        default=timezone.now,
    )
    loaded_image_quantity = models.IntegerField(
        default=0,
        blank=False,
    )
    max_image_quantity = models.IntegerField(
        blank=False,
    )
