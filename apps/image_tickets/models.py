from django.db import models

class TicketStatus(models.TextChoices):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'

class Ticket(models.Model):
    number_of_images = models.IntegerField(
        blank=False,
    )
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
    created_at = models.DateTimeField(auto_now_add=True)
