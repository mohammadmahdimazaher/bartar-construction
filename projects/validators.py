import json
from pathlib import Path

from django.core.exceptions import ValidationError


MAX_IMAGE_SIZE = 5 * 1024 * 1024
MAX_3D_MODEL_SIZE = 100 * 1024 * 1024


def validate_image_size(file):
    if file.size > MAX_IMAGE_SIZE:
        raise ValidationError("Image size must be under 5 MB.")


def validate_3d_model(file):
    extension = Path(file.name).suffix.lower()
    if extension not in {".glb", ".gltf"}:
        raise ValidationError("Only GLB and GLTF files are allowed.")

    if file.size > MAX_3D_MODEL_SIZE:
        raise ValidationError("3D model size must be under 100 MB.")

    # File extensions and browser-supplied MIME types are not trustworthy.
    # Check the GLB magic bytes or parse the GLTF JSON structure itself.
    try:
        file.seek(0)
        if extension == ".glb":
            if file.read(4) != b"glTF":
                raise ValidationError("The uploaded file is not a valid GLB model.")
        else:
            try:
                document = json.loads(file.read().decode("utf-8-sig"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                raise ValidationError("The uploaded file is not valid GLTF JSON.")

            if (
                not isinstance(document, dict)
                or not isinstance(document.get("asset"), dict)
                or not document["asset"].get("version")
            ):
                raise ValidationError("The uploaded file does not contain a valid GLTF asset header.")
    finally:
        file.seek(0)
