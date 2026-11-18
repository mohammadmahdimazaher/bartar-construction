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
