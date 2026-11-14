from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import SitePage
from .serializers import SitePageSerializer


class SitePageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SitePageSerializer
    permission_classes = [AllowAny]
    lookup_field = "key"

    def get_queryset(self):
        return SitePage.objects.filter(is_published=True).prefetch_related("gallery")
