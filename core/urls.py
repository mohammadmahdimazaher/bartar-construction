
from django.contrib import admin
from django.urls import path, include, re_path
import os

from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


API_DOCS_ENABLED = settings.DEBUG or os.getenv("API_DOCS_ENABLED", "False").lower() == "true"

schema_view = get_schema_view(
    openapi.Info(
        title="Start Up API",
        default_version="v1",
        description="API documentation for Start Up website",
    ),
    public=False,
    permission_classes=(permissions.IsAdminUser,),
)


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Language switch
    path("i18n/", include("django.conf.urls.i18n")),

    # Applications
    path("api/projects/", include("projects.urls")),
    path("api/pages/", include("pages.urls")),

    # API documentation is only exposed in development or when explicitly enabled.
]

if API_DOCS_ENABLED:
    urlpatterns += [
        re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
        re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    ]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
