
from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=500)

    is_for_sale = models.BooleanField(default=False)

    main_image = models.ImageField(
        upload_to="projects/main/",
        blank=True,
        null=True,
    )

    model_3d = models.FileField(
        upload_to="projects/3d/",
        blank=True,
        null=True,
    )

    parking_plan = models.ImageField(
        upload_to="projects/parking/",
        blank=True,
        null=True,
    )

    # Building details
    total_units = models.PositiveIntegerField(
        verbose_name="تعداد کل واحدها",
        null=True,
        blank=True,
    )

    floors_count = models.PositiveIntegerField(
        verbose_name="تعداد طبقات",
        null=True,
        blank=True,
    )

    building_width = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="عرض بنا",
    )

    units_per_floor = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="تعداد واحد هر طبقه",
    )

    useful_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="مساحت مفید طبقه",
    )

    # Facilities
    has_roof_garden = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="روف گاردن",
    )

    has_pool = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="استخر",
    )

    is_sloped_design = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="طراحی در شیب",
    )

    has_pilot = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="پیلوت",
    )

    pilot_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="متراژ پیلوت",
    )

    has_basement = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="زیرزمین",
    )

    basement_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="متراژ زیرزمین",
    )

    basement_plan = models.ImageField(
        upload_to="projects/basement/",
        null=True,
        blank=True,
        verbose_name="پلان زیرزمین",
    )

    has_game_room = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="اتاق بازی",
    )

    has_elevator = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="آسانسور",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UnitType(models.Model):
    DIRECTIONS = [
        ("north", "شمالی"),
        ("south", "جنوبی"),
        ("east", "شرقی"),
        ("west", "غربی"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="unit_types",
    )

    direction = models.CharField(
        max_length=10,
        choices=DIRECTIONS,
    )

    description = models.TextField()

    area = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
    )

    image = models.ImageField(
        upload_to="projects/units/images/",
        blank=True,
        null=True,
    )

    floor_plan = models.ImageField(
        upload_to="projects/units/floor_plans/",
        blank=True,
        null=True,
    )

    model_3d = models.FileField(
        upload_to="projects/units/3d/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.project.title} - {self.get_direction_display()}"
