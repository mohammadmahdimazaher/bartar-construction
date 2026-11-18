from django.contrib import admin
from django.utils.html import format_html

from .models import ConstructionReport, ConstructionStage, Project, UnitType



class ConstructionStageInline(admin.TabularInline):
    model = ConstructionStage
    extra = 0
    fields = ("order", "title", "weight", "progress", "is_completed", "start_date", "end_date", "notes")
    ordering = ("order",)


class ConstructionReportInline(admin.StackedInline):
    model = ConstructionReport
    extra = 0
    fields = ("stage", "title", "description", "report_date", "image", "is_public")
    ordering = ("-report_date",)


class UnitTypeInline(admin.StackedInline):
    model = UnitType
    extra = 0
    show_change_link = True
    classes = ("collapse",)

    fieldsets = (
        ("اطلاعات واحد", {
            "fields": (
                "direction",
                "description",
                "area",
                "image",
                "floor_plan",
                "model_3d",
            )
        }),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "project_title",
        "address",
        "project_image",
        "total_units",
        "floors_count",
        "sale_status",
        "construction_status",
        "created_at",
    )
    list_display_links = ("project_title",)
    list_filter = ("is_for_sale", "construction_status", "project_type", "structure_type", "is_published", "has_elevator", "has_basement", "has_pool", "has_roof_garden", "has_game_room")
    list_editable = ("address",)
    date_hierarchy = "created_at"
    list_select_related = ()
    search_fields = ("title", "address", "description")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 15
    empty_value_display = "ثبت نشده"
    save_on_top = True
    inlines = [UnitTypeInline, ConstructionStageInline, ConstructionReportInline]

    @admin.display(description="تصویر")
    def project_image(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="width:58px;height:42px;object-fit:cover;border-radius:7px;" />', obj.main_image.url)
        return "—"

    @admin.display(description="نام پروژه", ordering="title")
    def project_title(self, obj):
        return obj.title

    @admin.display(description="وضعیت اجرایی", ordering="construction_status")
    def construction_status(self, obj):
        return obj.get_construction_status_display()

    @admin.display(description="وضعیت فروش", boolean=True, ordering="is_for_sale")
    def sale_status(self, obj):
        return obj.is_for_sale

    fieldsets = (
        ("اطلاعات اصلی پروژه", {
            "fields": (
                "title",
                "description",
                "address",
                "main_image",
                "model_3d",
                "is_for_sale",
                "project_type",
                "structure_type",
                "is_published",
            )
        }),
        ("مدیریت پیشرفت و وضعیت اجرایی", {
            "fields": ("construction_status", "construction_start_date", "estimated_completion_date"),
        }),
        ("مشخصات کلی ساختمان", {
            "classes": ("collapse",),
            "fields": (
                "total_units",
                "floors_count",
                "units_per_floor",
                "building_width",
                "useful_area",
            )
        }),
        ("امکانات ساختمان", {
            "classes": ("collapse",),
            "fields": (
                "has_elevator",
                "has_roof_garden",
                "has_pool",
                "has_game_room",
                "is_sloped_design",
            )
        }),
        ("پیلوت و پارکینگ", {
            "classes": ("collapse",),
            "fields": (
                "has_pilot",
                "pilot_area",
                "parking_plan",
            )
        }),
        ("زیرزمین", {
            "classes": ("collapse",),
            "fields": (
                "has_basement",
                "basement_area",
                "basement_plan",
            )
        }),
    )


admin.site.site_header = "گروه ساختمانی برتر"
admin.site.site_title = "مدیریت برتر"
admin.site.index_title = "مرکز مدیریت مجموعه"
