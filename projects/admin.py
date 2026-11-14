from django.contrib import admin

from .models import Project, UnitType


class UnitTypeInline(admin.StackedInline):
    model = UnitType
    extra = 1
    show_change_link = True

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
        "title",
        "address",
        "total_units",
        "floors_count",
        "is_for_sale",
        "created_at",
    )
    list_filter = ("is_for_sale", "has_elevator", "has_basement")
    search_fields = ("title", "address")
    ordering = ("-created_at",)
    inlines = [UnitTypeInline]

    fieldsets = (
        ("اطلاعات اصلی پروژه", {
            "fields": (
                "title",
                "description",
                "address",
                "main_image",
                "model_3d",
                "is_for_sale",
            )
        }),
        ("مشخصات کلی ساختمان", {
            "fields": (
                "total_units",
                "floors_count",
                "units_per_floor",
                "building_width",
                "useful_area",
            )
        }),
        ("امکانات ساختمان", {
            "fields": (
                "has_elevator",
                "has_roof_garden",
                "has_pool",
                "has_game_room",
                "is_sloped_design",
            )
        }),
        ("پیلوت و پارکینگ", {
            "fields": (
                "has_pilot",
                "pilot_area",
                "parking_plan",
            )
        }),
        ("زیرزمین", {
            "fields": (
                "has_basement",
                "basement_area",
                "basement_plan",
            )
        }),
    )
