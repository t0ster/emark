from datetime import date, datetime

from django.test import TestCase
from django.core.exceptions import ValidationError

from core import models


class BaseTestCase(TestCase):
    def setUp(self):
        self.group = models.Group.objects.create(name="Test Group")
        self.semester = models.Semester.objects.create(
            start_date=date(2011, 2, 1),
            end_date=date(2011, 2, 15))
        self.subject = models.Subject.objects.create(
            name="Test Subject",
            group=self.group,
            semester=self.semester,
            start_datetime=datetime(2011, 2, 1, 10, 25)
        )


class SubjectTests(BaseTestCase):
    def test_get_lessons_datetimes(self):
        self.assertEqual(
            len(list(self.subject.get_lessons_datetimes())), 3)
        self.subject.per2weeks = True
        self.assertEqual(
            len(list(self.subject.get_lessons_datetimes())), 2)

    def test_validate_start_datetime(self):
        self.subject.start_datetime = datetime(2011, 2, 22, 10, 25)
        self.assertRaises(
            ValidationError,
            lambda: self.subject.save()
        )


class LessonTests(BaseTestCase):
    def test_lessons(self):
        self.assertEqual(
            models.Lesson.objects.count(), 3)

    def test_filter_by_weekday(self):
        tuesday_subjects = models.Lesson.objects.filter_by_weekday(
            weekday=1, week=1, semester=self.semester)
        self.assertEqual(tuesday_subjects.count(), 1)

    def test_iter_by_weekdays(self):
        self.assertTrue(models.Lesson.objects.iter_by_weekdays())
