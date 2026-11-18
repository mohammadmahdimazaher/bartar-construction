from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
import struct

from .models import ConstructionReport, ConstructionStage, Project, UnitType
from .validators import validate_3d_model
from .views import UnitTypeViewSet


class UploadSecurityTests(TestCase):
    def test_glb_requires_valid_magic_header(self):
        upload = SimpleUploadedFile("model.glb", b"<html>not a model</html>")
        with self.assertRaises(ValidationError):
            validate_3d_model(upload)

    def test_valid_glb_2_header_is_accepted(self):
        header = struct.pack("<4sII", b"glTF", 2, 12)
        upload = SimpleUploadedFile("model.glb", header)
        validate_3d_model(upload)

    def test_gltf_requires_valid_asset_document(self):
        upload = SimpleUploadedFile("model.gltf", b'{"scenes": []}')
        with self.assertRaises(ValidationError):
            validate_3d_model(upload)

    def test_valid_gltf_2_asset_document_is_accepted(self):
        upload = SimpleUploadedFile("model.gltf", b'{"asset": {"version": "2.0"}}')
        validate_3d_model(upload)


class ConstructionProgressTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="پروژه آزمایشی",
            description="توضیحات",
            address="تهران",
            construction_status="in_progress",
        )

    def test_weighted_progress_is_calculated(self):
        ConstructionStage.objects.create(
            project=self.project, title="فونداسیون", weight=2, progress=100,
        )
        ConstructionStage.objects.create(
            project=self.project, title="اسکلت", weight=3, progress=40,
        )
        self.assertEqual(self.project.construction_progress, 64)

    def test_completed_stage_is_marked_as_fully_complete(self):
        stage = ConstructionStage.objects.create(
            project=self.project, title="فونداسیون", progress=35, is_completed=True,
        )
        self.assertEqual(stage.progress, 100)

    def test_progress_is_bounded_to_one_hundred(self):
        stage = ConstructionStage.objects.create(
            project=self.project, title="اسکلت", progress=140,
        )
        self.assertEqual(stage.progress, 100)
        self.assertTrue(stage.is_completed)

    def test_completed_project_is_not_reported_as_in_progress(self):
        self.project.construction_status = "completed"
        self.project.save()
        self.assertNotEqual(self.project.construction_status, "in_progress")


class ProjectLifecycleRulesTests(TestCase):
    def test_new_projects_default_to_completed(self):
        project = Project.objects.create(
            title="پروژه جدید",
            description="توضیحات",
            address="تهران",
        )
        self.assertEqual(project.construction_status, "completed")

    def test_projects_not_completed_cannot_be_for_sale(self):
        project = Project.objects.create(
            title="پروژه در حال ساخت",
            description="توضیحات",
            address="تهران",
            construction_status="in_progress",
            is_for_sale=True,
        )
        project.refresh_from_db()
        self.assertFalse(project.is_for_sale)

    def test_upcoming_projects_cannot_be_for_sale(self):
        project = Project.objects.create(
            title="پروژه آینده",
            description="توضیحات",
            address="تهران",
            construction_status="upcoming",
            is_for_sale=True,
        )
        project.refresh_from_db()
        self.assertFalse(project.is_for_sale)

    def test_completed_projects_can_be_marked_for_sale(self):
        project = Project.objects.create(
            title="پروژه تکمیل‌شده",
            description="توضیحات",
            address="تهران",
            construction_status="completed",
            is_for_sale=True,
        )
        self.assertTrue(project.is_for_sale)


class PublicProjectApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unpublished_projects_are_not_publicly_listed(self):
        Project.objects.create(
            title="پروژه عمومی", description="توضیحات", address="تهران",
            is_published=True,
        )
        Project.objects.create(
            title="پروژه خصوصی", description="توضیحات", address="تهران",
            is_published=False,
        )

        response = self.client.get(reverse("project-list"))

        self.assertEqual(response.status_code, 200)
        titles = [item["title"] for item in response.data]
        self.assertEqual(titles, ["پروژه عمومی"])

    def test_project_api_does_not_allow_anonymous_writes(self):
        response = self.client.post(
            reverse("project-list"),
            {"title": "تزریق", "description": "test", "address": "test"},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_completed_project_does_not_expose_progress(self):
        project = Project.objects.create(
            title="پروژه تکمیل‌شده", description="توضیحات", address="تهران",
            construction_status="completed",
        )
        ConstructionStage.objects.create(
            project=project, title="فونداسیون", progress=75,
        )

        response = self.client.get(reverse("project-list"))

        self.assertEqual(response.status_code, 200)
        item = next(item for item in response.data if item["id"] == project.id)
        self.assertIsNone(item["construction_progress"])
        self.assertEqual(item["construction_stages"], [])

    def test_only_public_construction_reports_are_exposed(self):
        project = Project.objects.create(
            title="پروژه در حال ساخت", description="توضیحات", address="تهران",
            construction_status="in_progress",
        )
        ConstructionReport.objects.create(
            project=project, title="گزارش عمومی", description="متن",
            report_date="2026-01-01", is_public=True,
        )
        ConstructionReport.objects.create(
            project=project, title="گزارش داخلی", description="متن",
            report_date="2026-01-02", is_public=False,
        )

        response = self.client.get(reverse("project-list"))

        self.assertEqual(response.status_code, 200)
        item = next(item for item in response.data if item["id"] == project.id)
        report_titles = [report["title"] for report in item["construction_reports"]]
        self.assertEqual(report_titles, ["گزارش عمومی"])

    def test_unit_type_queryset_excludes_unpublished_projects(self):
        public_project = Project.objects.create(
            title="عمومی", description="توضیحات", address="تهران",
            is_published=True,
        )
        private_project = Project.objects.create(
            title="خصوصی", description="توضیحات", address="تهران",
            is_published=False,
        )
        public_unit = UnitType.objects.create(
            project=public_project, direction="north", description="واحد عمومی",
        )
        private_unit = UnitType.objects.create(
            project=private_project, direction="south", description="واحد خصوصی",
        )

        queryset = UnitTypeViewSet().get_queryset()

        self.assertTrue(queryset.filter(pk=public_unit.pk).exists())
        self.assertFalse(queryset.filter(pk=private_unit.pk).exists())
