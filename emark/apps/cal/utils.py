# -*- coding: utf-8 -*-
from itertools import izip_longest
from collections import namedtuple

from django.utils.translation import ugettext as _

from emark.utils import unique_everseen
from core.models import Subject


WEEKDAYS = (
    _(u"Пон"),
    _(u"Вт"),
    _(u"Ср"),
    _(u"Чет"),
    _(u"Пят"),
    _(u"Суб"),
    _(u"Вос"),
)


DummySubject = namedtuple("Subject", "start_datetime")


class Calendar(object):
    def __init__(self, semester=None):
        self.semester = semester

    def iter_by_weekdays(self):
        week1, week2 = AppendedWeeks(
            Subject.objects.iter_by_weekdays(week=1, semester=self.semester),
            Subject.objects.iter_by_weekdays(week=2, semester=self.semester)
            ).get()
        result = [list(izip_longest(w1, w2)) for w1, w2 in
                  list(izip_longest(week1, week2))]
        return zip(WEEKDAYS, result)


class AppendedWeeks(object):
    def __init__(self, week1, week2):
        self.week1 = list(week1)
        self.week2 = list(week2)

    def get_times(self, week1, week2):
        week1_times = [[subj.start_datetime for subj in d] for d in week1]
        week2_times = [[subj.start_datetime for subj in d] for d in week2]

        return [
            sorted(unique_everseen(set(times_week1) | set(times_week2), lambda x: x.time())) for
            times_week1, times_week2 in
            zip(week1_times, week2_times)
        ]

    def get_from_day_by_time(self, day, time, default=None):
        try:
            return [s for s in day if s.start_datetime.time() == time.time()][0]
        except IndexError:
            return default

    def get_appended_week(self, week, times):
        new_week = []
        for day_times, day in zip(times, week):
            lessons = []
            for _time in day_times:
                lessons.append(
                    self.get_from_day_by_time(
                        day, _time,
                        DummySubject(_time)))
            new_week.append(lessons)
        return new_week

    def get(self):
        times = self.get_times(self.week1, self.week2)
        return (
            self.get_appended_week(self.week1, times),
            self.get_appended_week(self.week2, times)
        )
