
from pathlib import Path

from django.core.exceptions import ValidationError


def validate_image_size(file):
    if file.size > 5 * 1024 * 1024:
        raise ValidationError("Image size must be under 5 MB.")


def validate_3d_model(file):
    extension = Path(file.name).suffix.lower()

    if extension not in [".glb", ".gltf"]:
        raise ValidationError("Only GLB and GLTF files are allowed.")

    if file.size > 100 * 1024 * 1024:
        raise ValidationError("3D model size must be under 100 MB.")
