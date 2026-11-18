
from django.db import models

from .validators import validate_image_size


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


    # Project classification and execution lifecycle
    PROJECT_TYPES = [
        ("residential", "مسکونی"),
        ("commercial", "تجاری"),
        ("office", "اداری"),
        ("industrial", "صنعتی"),
        ("mixed_use", "مجتمع چندمنظوره"),
        ("villa", "ویلایی"),
        ("other", "سایر"),
    ]
    STRUCTURE_TYPES = [
        ("concrete", "اسکلت بتنی"),
        ("steel", "اسکلت فلزی"),
        ("load_bearing", "دیوار باربر"),
        ("lsf", "سازه سبک فولادی (LSF)"),
        ("other", "سایر"),
    ]
    CONSTRUCTION_STATUSES = [
        ("upcoming", "به‌زودی"),
        ("in_progress", "در حال ساخت"),
        ("completed", "اتمام ساخت"),
    ]

    project_type = models.CharField(
        max_length=20, choices=PROJECT_TYPES, default="residential",
        verbose_name="نوع پروژه",
    )
    structure_type = models.CharField(
        max_length=20, choices=STRUCTURE_TYPES, default="other",
        verbose_name="نوع سیستم سازه‌ای",
    )
    construction_status = models.CharField(
        max_length=20, choices=CONSTRUCTION_STATUSES, default="completed",
        db_index=True, verbose_name="وضعیت اجرایی",
    )
    is_published = models.BooleanField(
        default=True, db_index=True, verbose_name="نمایش در سایت",
    )
    construction_start_date = models.DateField(
        null=True, blank=True, verbose_name="تاریخ شروع ساخت",
    )
    estimated_completion_date = models.DateField(
        null=True, blank=True, verbose_name="تاریخ پیش‌بینی‌شده اتمام",
    )

    @property
    def construction_progress(self):
        stages = list(self.construction_stages.all())
        total_weight = sum(stage.weight for stage in stages)
        if not total_weight:
            return 0
        return round(
            sum(stage.progress * stage.weight for stage in stages) / total_weight
        )

    def save(self, *args, **kwargs):
        # A project can only be offered for sale after construction is complete.
        if self.construction_status != "completed":
            self.is_for_sale = False
        super().save(*args, **kwargs)

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



class ConstructionStage(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="construction_stages",
        verbose_name="پروژه",
    )
    title = models.CharField(max_length=180, verbose_name="مرحله ساخت")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    weight = models.PositiveIntegerField(default=1, verbose_name="وزن در محاسبه پیشرفت")
    progress = models.PositiveSmallIntegerField(default=0, verbose_name="درصد پیشرفت")
    is_completed = models.BooleanField(default=False, verbose_name="تکمیل شده")
    start_date = models.DateField(null=True, blank=True, verbose_name="تاریخ شروع")
    end_date = models.DateField(null=True, blank=True, verbose_name="تاریخ پایان")
    notes = models.TextField(blank=True, verbose_name="توضیحات")

    class Meta:
        ordering = ("order", "id")
        verbose_name = "مرحله ساخت"
        verbose_name_plural = "مراحل ساخت"

    def save(self, *args, **kwargs):
        self.progress = min(100, max(0, self.progress))
        if self.is_completed:
            self.progress = 100
        elif self.progress == 100:
            self.is_completed = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project.title} - {self.title}"


class ConstructionReport(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="construction_reports",
        verbose_name="پروژه",
    )
    stage = models.ForeignKey(
        ConstructionStage, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="reports", verbose_name="مرحله مرتبط",
    )
    title = models.CharField(max_length=200, verbose_name="عنوان گزارش")
    description = models.TextField(verbose_name="متن گزارش")
    report_date = models.DateField(verbose_name="تاریخ گزارش")
    image = models.ImageField(
        upload_to="projects/reports/", null=True, blank=True,
        validators=[validate_image_size], verbose_name="تصویر گزارش",
    )
    is_public = models.BooleanField(default=True, verbose_name="نمایش عمومی گزارش")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-report_date", "-created_at")
        verbose_name = "گزارش پیشرفت"
        verbose_name_plural = "گزارش‌های پیشرفت"

    def __str__(self):
        return f"{self.project.title} - {self.title}"
