from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from celery import chain

from apps.image_tickets.models import Ticket, TicketStatus
from apps.image_tickets.serializers import ImageUploadSerializer, TicketSerializer
from apps.image_tickets.tasks import (
    update_ticket,
    upload_image_into_cloud_storage,
)
from apps.image_tickets.types import (
    CreateTicketSuccessResponse,
    GetPaginatedTicketsSuccessResponse,
    UploadImageSuccessResponse,
    page_param,
    per_page_param,
    start_date_param,
    end_date_param,
    status_param,
)
from apps.utils.common.types import GeneralErrorResponse
from apps.utils.constants import token_param
from apps.utils.utils import paginate_object


@swagger_auto_schema(
    method="get",
    responses={
        status.HTTP_200_OK: "Tickets found",
        status.HTTP_404_NOT_FOUND: "Tickets not found",
    },
    tags=["tickets"],
    manual_parameters=[
        token_param,
        page_param,
        per_page_param,
        start_date_param,
        end_date_param,
        status_param,
    ],
)
@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "max_image_quantity": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
        required=["max_image_quantity"],
    ),
    responses={
        status.HTTP_201_CREATED: "Created",
        status.HTTP_400_BAD_REQUEST: "Bad Request",
    },
    tags=["tickets"],
    manual_parameters=[token_param],
)
@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def ticket_view(request):
    print("request", request)
    if request.method == "POST":
        return create_ticket(request)
    elif request.method == "GET":
        return get_paginated_tickets(request)


def create_ticket(request):
    serializer = TicketSerializer(data={**request.data, "created_by": request.user.id})
    if not serializer.is_valid():
        return GeneralErrorResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)
    ticket = serializer.create(serializer.validated_data)
    return CreateTicketSuccessResponse({**serializer.data, "id": ticket.id})


@swagger_auto_schema(
    method="get",
    responses={
        status.HTTP_200_OK: "Ticket found",
        status.HTTP_404_NOT_FOUND: "Ticket not found",
    },
    tags=["tickets"],
    manual_parameters=[token_param],
)
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_by_id(request, pk):
    try:
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return GeneralErrorResponse("Ticket not found", status.HTTP_404_NOT_FOUND)
    serializer = TicketSerializer(ticket)
    return Response(serializer.data)


def get_paginated_tickets(request):
    page = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 10)
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    status = request.GET.get("status")

    tickets = get_filtered_tickets(status, start_date, end_date, request.user)
    tickets = paginate_object(tickets, page, per_page)

    serializer = TicketSerializer(tickets, many=True)
    return GetPaginatedTicketsSuccessResponse(serializer.data)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "image_url": openapi.Schema(
                type=openapi.TYPE_STRING, pattern="^https://.+"
            ),
        },
        required=["image_url"],
    ),
    responses={
        status.HTTP_202_ACCEPTED: "Received image",
        status.HTTP_400_BAD_REQUEST: "Ticket already completed",
        status.HTTP_404_NOT_FOUND: "Not found ticket",
    },
    tags=["tickets"],
    manual_parameters=[token_param],
)
@api_view(["POST"])
def upload_image(request, pk):
    try:
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return GeneralErrorResponse("Ticket not found", status.HTTP_404_NOT_FOUND)

    if ticket.status == TicketStatus.COMPLETED:
        return GeneralErrorResponse(
            "Ticket already completed", status.HTTP_400_BAD_REQUEST
        )

    serializer = ImageUploadSerializer(data=request.data)
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)

    image_url = serializer.validated_data.get("image_url")
    task_chain = chain(
        upload_image_into_cloud_storage.s(image_url),
        update_ticket.s(pk),
    )
    task_chain.apply_async()

    return UploadImageSuccessResponse()


def get_filtered_tickets(
    status: TicketStatus,
    start_date: str,
    end_date: str,
    user: User,
):
    tickets = Ticket.objects.filter(created_by=user)
    if start_date:
        tickets = tickets.filter(created_at__gte=start_date)
    if end_date:
        tickets = tickets.filter(created_at__lte=end_date)
    if status:
        tickets = tickets.filter(status=status)
    return tickets
