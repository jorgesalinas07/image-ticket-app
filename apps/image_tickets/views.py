from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.image_tickets.models import Ticket
from apps.image_tickets.serializers import TicketSerializer
from apps.image_tickets.types import CreateTicketSuccessResponse
from apps.utils.common.types import GeneralErrorResponse
from apps.utils.constants import token_param

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'number_of_images': openapi.Schema(type=openapi.TYPE_INTEGER),
        },
        required=['number_of_images']
    ),
    responses={
        status.HTTP_201_CREATED: 'Created',
        status.HTTP_400_BAD_REQUEST: 'Bad Request',
    },
    tags=['tickets'],
    manual_parameters=[token_param],
)
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_ticket(request):
    serializer = TicketSerializer(data={**request.data, 'created_by': request.user.id})
    if not serializer.is_valid():
        return GeneralErrorResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)
    serializer.create(serializer.validated_data)
    return CreateTicketSuccessResponse(serializer.data)
