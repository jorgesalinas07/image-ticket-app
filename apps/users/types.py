from rest_framework.response import Response
from rest_framework import status

class LoginSuccessResponse(Response):
    def __init__(self, token: str, user: dict):
        super().__init__(status=status.HTTP_200_OK, data={"token": token, "user": user})

class SignUpSuccessResponse(Response):
    def __init__(self, token: str, user: dict):
        super().__init__(status=status.HTTP_201_CREATED, data={"token": token, "user": user})
