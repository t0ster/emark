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
        self.subject1 = models.Subject.objects.create(
            name="Subject Mon 10:25",
            group=self.group,
            semester=self.semester,
            start_datetime=datetime(2011, 2, 7, 10, 25)
        )
        self.subject2 = models.Subject.objects.create(
            name="Subject Mon 12:20",
            group=self.group,
            semester=self.semester,
            start_datetime=datetime(2011, 2, 7, 12, 20)
        )
        self.subject3 = models.Subject.objects.create(
            name="Subject Tue 10:25",
            group=self.group,
            semester=self.semester,
            start_datetime=datetime(2011, 2, 1, 10, 25)
        )
        self.subject4 = models.Subject.objects.create(
            name="Subject Tue 12:20 per 2 weeks",
            group=self.group,
            semester=self.semester,
            start_datetime=datetime(2011, 2, 1, 10, 25),
            per2weeks=True,
        )


class SubjectTests(BaseTestCase):
    def test_get_lessons_datetimes(self):
        self.assertEqual(
            len(list(self.subject1.get_lessons_datetimes())), 2)

        self.subject1.per2weeks = True
        self.assertEqual(
            len(list(self.subject1.get_lessons_datetimes())), 1)

    def test_validate_start_datetime(self):
        self.subject1.start_datetime = datetime(2011, 2, 22, 10, 25)
        self.assertRaises(
            ValidationError,
            lambda: self.subject1.save()
        )

    def test_iter_by_weekdays(self):
        self.assertTrue(models.Subject.objects.iter_by_weekdays())


class FilterByWeekDayTests(BaseTestCase):
    def test_filter_by_weekday(self):
        mon_subjects = models.Subject.objects.filter_by_weekday(
            weekday=0, week=1, semester=self.semester)
        self.assertEqual(mon_subjects.count(), 2)

        tue_subjects = models.Subject.objects.filter_by_weekday(
            weekday=1, week=1, semester=self.semester)
        self.assertEqual(tue_subjects.count(), 2)

    def test_per2weeks(self):
        tue_subjects = models.Subject.objects.filter_by_weekday(
            weekday=1, week=2, semester=self.semester)
        self.assertEqual(tue_subjects.count(), 1)

    def test_semester_starts_1stweek(self):
        self.semester.starts_from_1st_week = False
        self.semester.save()

        tue_subjects = models.Subject.objects.filter_by_weekday(
            weekday=1, week=2, semester=self.semester)
        self.assertEqual(tue_subjects.count(), 2)


class LessonTests(BaseTestCase):
    def test_lessons(self):
        self.assertEqual(
            models.Lesson.objects.count(), 9)
