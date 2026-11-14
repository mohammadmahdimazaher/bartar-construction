from django.contrib import admin

from .models import SitePage, SitePageImage


class SitePageImageInline(admin.TabularInline):
    model = SitePageImage
    extra = 2


@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "is_published", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title", "content")
    inlines = [SitePageImageInline]
