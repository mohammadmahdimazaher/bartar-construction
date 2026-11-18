from django.test import TestCase
from .models import ConstructionStage, Project


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

    def test_completed_projects_can_be_marked_for_sale(self):
        project = Project.objects.create(
            title="پروژه تکمیل‌شده",
            description="توضیحات",
            address="تهران",
            construction_status="completed",
            is_for_sale=True,
        )
        self.assertTrue(project.is_for_sale)
