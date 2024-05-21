from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


def home(request):
    return HttpResponse("Hello, World!")


schema_view = get_schema_view(
    openapi.Info(
        title="Ticket App API",
        default_version="v1",
        description="Ticket App API",
    ),
    public=True,
)

urlpatterns = [
    path("users/", include("apps.users.urls")),
    path("tickets", include("apps.image_tickets.urls")),
    path("", home),
    path("admin/", admin.site.urls),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
