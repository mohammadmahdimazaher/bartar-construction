from rest_framework import serializers
from .models import ConstructionReport, ConstructionStage, Project, UnitType


class UnitTypeSerializer(serializers.ModelSerializer):
    direction_display = serializers.CharField(
        source="get_direction_display",
        read_only=True
    )

    class Meta:
        model = UnitType
        fields = "__all__"


class ConstructionStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionStage
        fields = "__all__"


class ConstructionReportSerializer(serializers.ModelSerializer):
    stage_title = serializers.CharField(source="stage.title", read_only=True)

    class Meta:
        model = ConstructionReport
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    unit_types = UnitTypeSerializer(many=True, read_only=True)
    construction_stages = serializers.SerializerMethodField()
    construction_reports = serializers.SerializerMethodField()
    construction_progress = serializers.SerializerMethodField()

    def get_construction_stages(self, obj):
        if obj.construction_status not in ("in_progress",):
            return []
        return ConstructionStageSerializer(obj.construction_stages.all(), many=True, context=self.context).data

    def get_construction_reports(self, obj):
        if obj.construction_status not in ("in_progress", "paused"):
            return []
        reports = obj.construction_reports.filter(is_public=True)
        return ConstructionReportSerializer(reports, many=True, context=self.context).data

    def get_construction_progress(self, obj):
        if obj.construction_status not in ("in_progress", "paused"):
            return None
        return obj.construction_progress

    class Meta:
        model = Project
        fields = "__all__"



