# Generated for project construction lifecycle and progress tracking.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0009_alter_project_options_alter_unittype_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="project_type",
            field=models.CharField(choices=[("residential", "مسکونی"), ("commercial", "تجاری"), ("office", "اداری"), ("industrial", "صنعتی"), ("mixed_use", "مجتمع چندمنظوره"), ("villa", "ویلایی"), ("other", "سایر")], default="residential", max_length=20, verbose_name="نوع پروژه"),
        ),
        migrations.AddField(
            model_name="project",
            name="structure_type",
            field=models.CharField(choices=[("concrete", "اسکلت بتنی"), ("steel", "اسکلت فلزی"), ("load_bearing", "دیوار باربر"), ("lsf", "سازه سبک فولادی (LSF)"), ("other", "سایر")], default="other", max_length=20, verbose_name="نوع سیستم سازه‌ای"),
        ),
        migrations.AddField(
            model_name="project",
            name="construction_status",
            field=models.CharField(choices=[("planning", "در حال برنامه‌ریزی"), ("pending", "در انتظار شروع"), ("in_progress", "در حال ساخت"), ("paused", "متوقف‌شده"), ("completed", "تکمیل‌شده"), ("delivered", "تحویل‌شده"), ("archived", "بایگانی‌شده")], db_index=True, default="planning", max_length=20, verbose_name="وضعیت اجرایی"),
        ),
        migrations.AddField(
            model_name="project",
            name="is_published",
            field=models.BooleanField(db_index=True, default=True, verbose_name="نمایش در سایت"),
        ),
        migrations.AddField(
            model_name="project",
            name="construction_start_date",
            field=models.DateField(blank=True, null=True, verbose_name="تاریخ شروع ساخت"),
        ),
        migrations.AddField(
            model_name="project",
            name="estimated_completion_date",
            field=models.DateField(blank=True, null=True, verbose_name="تاریخ پیش‌بینی‌شده اتمام"),
        ),
        migrations.CreateModel(
            name="ConstructionStage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180, verbose_name="مرحله ساخت")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")),
                ("weight", models.PositiveIntegerField(default=1, verbose_name="وزن در محاسبه پیشرفت")),
                ("progress", models.PositiveSmallIntegerField(default=0, verbose_name="درصد پیشرفت")),
                ("is_completed", models.BooleanField(default=False, verbose_name="تکمیل شده")),
                ("start_date", models.DateField(blank=True, null=True, verbose_name="تاریخ شروع")),
                ("end_date", models.DateField(blank=True, null=True, verbose_name="تاریخ پایان")),
                ("notes", models.TextField(blank=True, verbose_name="توضیحات")),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="construction_stages", to="projects.project", verbose_name="پروژه")),
            ],
            options={"verbose_name": "مرحله ساخت", "verbose_name_plural": "مراحل ساخت", "ordering": ("order", "id")},
        ),
        migrations.CreateModel(
            name="ConstructionReport",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="عنوان گزارش")),
                ("description", models.TextField(verbose_name="متن گزارش")),
                ("report_date", models.DateField(verbose_name="تاریخ گزارش")),
                ("image", models.ImageField(blank=True, null=True, upload_to="projects/reports/", verbose_name="تصویر گزارش")),
                ("is_public", models.BooleanField(default=True, verbose_name="نمایش عمومی گزارش")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="construction_reports", to="projects.project", verbose_name="پروژه")),
                ("stage", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="reports", to="projects.constructionstage", verbose_name="مرحله مرتبط")),
            ],
            options={"verbose_name": "گزارش پیشرفت", "verbose_name_plural": "گزارش‌های پیشرفت", "ordering": ("-report_date", "-created_at")},
        ),
    ]
