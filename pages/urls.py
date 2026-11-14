from rest_framework.routers import DefaultRouter

from .views import SitePageViewSet

router = DefaultRouter()
router.register("sections", SitePageViewSet, basename="sections")

urlpatterns = router.urls
