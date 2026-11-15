from django.contrib import admin

from .models import SitePage, SitePageImage


class SitePageImageInline(admin.TabularInline):
    model = SitePageImage
    extra = 1
    ordering = ("order",)
    fields = ("image", "order")
    verbose_name = "تصویر گالری"
    verbose_name_plural = "گالری تصاویر این بخش"


@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    list_display = ("page_title", "key", "publication_status", "gallery_count", "updated_at")
    list_display_links = ("page_title",)
    list_filter = ("is_published", "key")
    search_fields = ("title", "subtitle", "content")
    ordering = ("key",)
    list_per_page = 20
    save_on_top = True
    inlines = [SitePageImageInline]
    readonly_fields = ("updated_at",)

    fieldsets = (
        ("محتوای اصلی", {
            "fields": ("key", "title", "subtitle", "content", "is_published")
        }),
        ("رسانه اصلی", {
            "fields": ("image",)
        }),
        ("اطلاعات سیستمی", {
            "classes": ("collapse",),
            "fields": ("updated_at",)
        }),
    )

    @admin.display(description="عنوان بخش", ordering="title")
    def page_title(self, obj):
        return obj.title

    @admin.display(description="وضعیت انتشار", boolean=True, ordering="is_published")
    def publication_status(self, obj):
        return obj.is_published

    @admin.display(description="تعداد تصاویر")
    def gallery_count(self, obj):
        return obj.gallery.count()
