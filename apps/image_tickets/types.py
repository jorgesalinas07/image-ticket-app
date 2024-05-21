from typing import List
from rest_framework.response import Response
from rest_framework import status

from drf_yasg import openapi


class CreateTicketSuccessResponse(Response):
    def __init__(self, ticket: dict):
        super().__init__(status=status.HTTP_201_CREATED, data={"ticket": ticket})


class UploadImageSuccessResponse(Response):
    def __init__(self):
        super().__init__(
            status=status.HTTP_202_ACCEPTED,
            data="Image upload request received successfully",
        )


class GetPaginatedTicketsSuccessResponse(Response):
    def __init__(self, tickets: List[dict]):
        super().__init__(status=status.HTTP_200_OK, data={tickets})


page_param = openapi.Parameter(  ## Move this to utils or somewhere else
    "page",
    in_=openapi.IN_QUERY,
    description="Page",
    type=openapi.TYPE_INTEGER,
    default=1,
)

per_page_param = openapi.Parameter(
    "per_page",
    in_=openapi.IN_QUERY,
    description="Number of tickets per page",
    type=openapi.TYPE_INTEGER,
    default=10,
)

start_date_param = openapi.Parameter(
    "start_date",
    in_=openapi.IN_QUERY,
    description="Start date to filter (Format: YYYY-MM-DD)",
    type=openapi.TYPE_STRING,
    format=openapi.FORMAT_DATE,
)

end_date_param = openapi.Parameter(
    "end_date",
    in_=openapi.IN_QUERY,
    description="End date to filter (Format: YYYY-MM-DD)",
    type=openapi.TYPE_STRING,
    format=openapi.FORMAT_DATE,
)

status_param = openapi.Parameter(
    "status",
    in_=openapi.IN_QUERY,
    description="Ticket status (Options: PENDING/COMPLETED)",
    type=openapi.TYPE_STRING,
    enum=["PENDING", "COMPLETED"],
)
