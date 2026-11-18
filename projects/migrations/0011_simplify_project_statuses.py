# Restrict project lifecycle to the three business statuses.
from django.db import migrations, models


def mark_existing_projects_completed(apps, schema_editor):
    Project = apps.get_model("projects", "Project")
    Project.objects.all().update(construction_status="completed")


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0010_project_construction_lifecycle"),
    ]

    operations = [
        migrations.RunPython(
            mark_existing_projects_completed,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="project",
            name="construction_status",
            field=models.CharField(
                choices=[
                    ("upcoming", "به‌زودی"),
                    ("in_progress", "در حال ساخت"),
                    ("completed", "اتمام ساخت"),
                ],
                db_index=True,
                default="completed",
                max_length=20,
                verbose_name="وضعیت اجرایی",
            ),
        ),
    ]
