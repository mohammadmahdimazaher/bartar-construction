from django.apps import apps
from django.db.models import Count


def bartar_admin_dashboard(request):
    if not request.path.startswith("/admin/") or not getattr(request.user, "is_staff", False):
        return {}

    Project = apps.get_model("projects", "Project")
    UnitType = apps.get_model("projects", "UnitType")
    SitePage = apps.get_model("pages", "SitePage")
    SitePageImage = apps.get_model("pages", "SitePageImage")

    projects = Project.objects.order_by("-created_at")
    return {
        "bartar_stats": {
            "projects": projects.count(),
            "sale": projects.filter(is_for_sale=True).count(),
            "units": UnitType.objects.count(),
            "published_pages": SitePage.objects.filter(is_published=True).count(),
            "draft_pages": SitePage.objects.filter(is_published=False).count(),
            "media": (
                Project.objects.exclude(main_image="").count()
                + SitePage.objects.exclude(image="").count()
                + SitePageImage.objects.count()
            ),
        },
        "bartar_recent_projects": projects[:6],
    }
