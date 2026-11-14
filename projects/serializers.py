from rest_framework import serializers
from .models import Project, UnitType


class UnitTypeSerializer(serializers.ModelSerializer):
    direction_display = serializers.CharField(
        source="get_direction_display",
        read_only=True
    )

    class Meta:
        model = UnitType
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    unit_types = UnitTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
