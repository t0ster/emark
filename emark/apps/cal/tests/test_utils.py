from datetime import datetime, date, time, timedelta

from mocker import MockerTestCase

from cal.utils import AppendedWeeks, Calendar, DummySubject
from core.tests.test_models import BaseTestCase


class AppendedWeeksTests(MockerTestCase):
    def setUp(self):
        self._10_25 = datetime.combine(date.today(), time(10, 25))
        self._12_20 = datetime.combine(date.today(), time(12, 20))
        self._14_15 = datetime.combine(date.today(), time(14, 15))

        self.week1 = [[]]
        for _dt in (self._10_25, self._14_15):
            sub = self.mocker.mock("Subject")
            sub.start_datetime
            self.mocker.result(_dt)
            self.mocker.count(None, None)
            self.week1[0].append(sub)

        sub = self.mocker.mock("Subject")
        sub.start_datetime
        self.mocker.result(self._12_20)
        self.mocker.count(None, None)
        self.week2 = [[sub]]

    def test_appended_weeks(self):
        self.mocker.replay()

        new_week1, new_week2 = AppendedWeeks(self.week1, self.week2).get()
        for day in new_week1:
            for subj, _dt in zip(day, (self._10_25, self._12_20, self._14_15)):
                self.assertEqual(subj.start_datetime, _dt)
        for day in new_week2:
            for subj, _dt in zip(day, (self._10_25, self._12_20, self._14_15)):
                self.assertEqual(subj.start_datetime, _dt)

    def test_weeks_1_2(self):
        sub = self.mocker.mock("Subject")
        sub.start_datetime
        self.mocker.result(self._10_25)
        self.mocker.count(None, None)
        week1 = [[sub]]

        sub = self.mocker.mock("Subject")
        sub.start_datetime
        self.mocker.result(self._10_25 + timedelta(7))
        self.mocker.count(None, None)
        week2 = [[sub]]

        self.mocker.replay()

        new_week1, new_week2 = AppendedWeeks(week1, week2).get()

        self.assertEqual(len(new_week1[0]), 1)
        self.assertNotEqual(type(new_week1[0][0]), DummySubject)


class CalendarTests(BaseTestCase):
    def test_calendar(self):
        self.assertTrue(Calendar(self.semester).iter_by_weekdays())
