from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.image_tickets.models import Ticket
from apps.image_tickets.serializers import TicketSerializer
from apps.image_tickets.types import CreateTicketSuccessResponse
from apps.utils.common.types import GeneralErrorResponse
from apps.utils.constants import token_param

page_param = openapi.Parameter( ## Move this to utils or somewhere else
    'page',
    in_=openapi.IN_QUERY,
    description='Page',
    type=openapi.TYPE_INTEGER,
    default=1
)

per_page_param = openapi.Parameter(
    'per_page',
    in_=openapi.IN_QUERY,
    description='Number of tickets per page',
    type=openapi.TYPE_INTEGER,
    default=10
)

start_date_param = openapi.Parameter(
    'start_date',
    in_=openapi.IN_QUERY,
    description='Start date to filter (Format: YYYY-MM-DD)',
    type=openapi.TYPE_STRING,
    format=openapi.FORMAT_DATE
)

end_date_param = openapi.Parameter(
    'end_date',
    in_=openapi.IN_QUERY,
    description='End date to filter (Format: YYYY-MM-DD)',
    type=openapi.TYPE_STRING,
    format=openapi.FORMAT_DATE
)

status_param = openapi.Parameter(
    'status',
    in_=openapi.IN_QUERY,
    description='Ticket status (Options: PENDING/COMPLETED)',
    type=openapi.TYPE_STRING,
    enum=['PENDING', 'COMPLETED'],
)

@swagger_auto_schema( ## Move this to utils
    method='get',
    responses={
        status.HTTP_200_OK: 'Tickets found',
        status.HTTP_404_NOT_FOUND: 'Tickets not found',
    },
    tags=['tickets'],
    manual_parameters=[
        token_param,
        page_param,
        per_page_param,
        start_date_param,
        end_date_param,
        status_param
    ],
)
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'max_image_quantity': openapi.Schema(type=openapi.TYPE_INTEGER),
        },
        required=['max_image_quantity']
    ),
    responses={
        status.HTTP_201_CREATED: 'Created',
        status.HTTP_400_BAD_REQUEST: 'Bad Request',
    },
    tags=['tickets'],
    manual_parameters=[token_param],
)
@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def ticket_view(request):
    print("request", request)
    if request.method == 'POST':
        return create_ticket(request)
    elif request.method == 'GET':
        return get_paginated_tickets(request)


def create_ticket(request):
    serializer = TicketSerializer(data={**request.data, 'created_by': request.user.id})
    if not serializer.is_valid():
        return GeneralErrorResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)
    serializer.create(serializer.validated_data)
    return CreateTicketSuccessResponse(serializer.data)


@swagger_auto_schema(
    method='get',
    responses={
        status.HTTP_200_OK: 'Ticket found',
        status.HTTP_404_NOT_FOUND: 'Ticket not found',
    },
    tags=['tickets'],
    manual_parameters=[token_param],
)
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_by_id(request, pk):
    try:
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return GeneralErrorResponse('Ticket not found', status.HTTP_404_NOT_FOUND)
    serializer = TicketSerializer(ticket)
    return Response(serializer.data)


def get_paginated_tickets(request):
    print("request", request)
    page = request.GET.get('page', 1) ## Move this to utils that receives name and returns param
    per_page = request.GET.get('per_page', 10)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')
    print("filters", start_date, end_date, status, page, per_page)
    tickets = Ticket.objects.filter(created_by=request.user) ## Move this to a service (filters)
    if start_date:
        tickets = tickets.filter(created_at__gte=start_date)
    if end_date:
        tickets = tickets.filter(created_at__lte=end_date)
    if status:
        tickets = tickets.filter(status=status)

    # Paginate tickets
    paginator = Paginator(tickets, per_page) #  Move this to utils
    try:
        tickets = paginator.page(page)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)

    # # Serialize and return tickets
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data) ## Return custom error

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'image_url': openapi.Schema(type=openapi.TYPE_INTEGER),
        },
        required=['image_url']
    ),
    responses={
        status.HTTP_202_ACCEPTED: 'Received image',
        status.HTTP_404_NOT_FOUND: 'Not found ticket',
    },
    tags=['tickets'],
    manual_parameters=[token_param],
)
@api_view(['POST'])
def upload_image(request, pk):
    try:
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return GeneralErrorResponse('Ticket not found', status.HTTP_404_NOT_FOUND)
    serializer = TicketSerializer(ticket)
    return Response(serializer.data) ## Return custom error
