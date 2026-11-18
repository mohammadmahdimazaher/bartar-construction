
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from .models import Project, UnitType
from .serializers import ProjectSerializer, UnitTypeSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.filter(is_published=True).prefetch_related(
        "unit_types", "construction_stages", "construction_reports",
    )
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UnitTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UnitType.objects.all()
    serializer_class = UnitTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
