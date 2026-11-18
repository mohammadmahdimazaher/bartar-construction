
from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from .models import ConstructionReport, Project, UnitType
from .serializers import ProjectSerializer, UnitTypeSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.filter(is_published=True).prefetch_related(
        "unit_types",
        "construction_stages",
        Prefetch(
            "construction_reports",
            queryset=ConstructionReport.objects.filter(is_public=True).select_related("stage"),
            to_attr="public_construction_reports",
        ),
    )
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UnitTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UnitTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return UnitType.objects.filter(project__is_published=True).select_related("project")
