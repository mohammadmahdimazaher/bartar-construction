# Add server-side validation to uploaded 3D assets.
from django.db import migrations, models
import projects.validators


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0011_simplify_project_statuses"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="model_3d",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="projects/3d/",
                validators=[projects.validators.validate_3d_model],
            ),
        ),
        migrations.AlterField(
            model_name="unittype",
            name="model_3d",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="projects/units/3d/",
                validators=[projects.validators.validate_3d_model],
            ),
        ),
    ]
