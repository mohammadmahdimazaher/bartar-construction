import json
import struct
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
    # Validate the binary GLB header or parse the GLTF JSON asset header.
    try:
        file.seek(0)
        if extension == ".glb":
            header = file.read(12)
            if len(header) != 12:
                raise ValidationError("The uploaded GLB file is incomplete.")
            magic, version, declared_length = struct.unpack("<4sII", header)
            if magic != b"glTF" or version != 2 or declared_length != file.size:
                raise ValidationError("The uploaded file is not a valid GLB 2.0 model.")
        else:
            try:
                document = json.loads(file.read().decode("utf-8-sig"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                raise ValidationError("The uploaded file is not valid GLTF JSON.")

            asset = document.get("asset") if isinstance(document, dict) else None
            version = asset.get("version") if isinstance(asset, dict) else None
            if not isinstance(version, str) or not version.startswith("2."):
                raise ValidationError("The uploaded file does not contain a valid GLTF 2.x asset header.")
    finally:
        file.seek(0)
