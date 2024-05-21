from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from apps.users.serializers import UserSerializer
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.users.types import LoginSuccessResponse, SignUpSuccessResponse
from apps.utils.common.types import GeneralErrorResponse
from apps.utils.constants import token_param


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.FORMAT_PASSWORD),
        },
        required=["username", "password"],
    ),
    responses={
        status.HTTP_200_OK: "Login successful",
        status.HTTP_404_NOT_FOUND: "User not Found",
    },
    tags=["users"],
)
@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return GeneralErrorResponse("Invalid password", status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return LoginSuccessResponse(token.key, serializer.data)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.FORMAT_PASSWORD),
            "email": openapi.Schema(type=openapi.FORMAT_EMAIL),
            "first_name": openapi.Schema(type=openapi.TYPE_STRING),
            "last_name": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["username", "password"],
    ),
    responses={
        status.HTTP_201_CREATED: "Created",
        status.HTTP_400_BAD_REQUEST: "Bad Request",
    },
    tags=["users"],
)
@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return SignUpSuccessResponse(token.key, serializer.data)
    return GeneralErrorResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="get",
    manual_parameters=[token_param],
    tags=["users"],
)
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("Passed for {}".format(request.user.username))
