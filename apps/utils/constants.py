from drf_yasg import openapi

token_param = openapi.Parameter(
    "Authorization",
    openapi.IN_HEADER,
    description="Format: token <insert-token>",
    type=openapi.TYPE_STRING,
    required=True,
)
