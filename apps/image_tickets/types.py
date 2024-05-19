from rest_framework.response import Response
from rest_framework import status

from apps.image_tickets.models import Ticket

class CreateTicketSuccessResponse(Response):
    def __init__(self, ticket):
        super().__init__(status=status.HTTP_201_CREATED, data={"ticket": ticket})
