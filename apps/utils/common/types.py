from rest_framework.response import Response


class GeneralErrorResponse(Response):
    def __init__(self, message: str, status: int = 500):
        super().__init__(status=status, data={"error": message})
