# -*- coding: utf-8 -*-
from itertools import izip_longest
from calendar import monthcalendar
from datetime import timedelta, datetime, date, time

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.dateformat import format as dateformat
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from emark.db.utils import ValidationManager
from core import conf


_(u"core")
_(u"Core")


class SemesterManager(ValidationManager):
    def get_current_semester(self):
        today = date.today()
        return self.get(start_date__lte=today, end_date__gte=today)


class Semester(models.Model):
    start_date = models.DateField(verbose_name=_(u"дата начала"), unique=True)
    end_date = models.DateField(verbose_name=_(u"дата конца"), unique=True)
    starts_from_1st_week = models.BooleanField(u"начинается с первой недели", default=True)

    def validate_date_end_gte_start(self):
        if self.start_date >= self.end_date:
            raise ValidationError(_(
                    u"Дата начала должна быть меньше."))

    def validate_date_edit(self):
        if self.pk:
            old_obj = Semester.objects.get(pk=self.pk)
            new_obj = self
            if (old_obj.start_date != new_obj.start_date or
                old_obj.end_date != new_obj.end_date):
                raise ValidationError(_(
                        u"Вы не можете редактировать даты существующего "
                        u"семестра. Вы можете удалить существующий семестр и "
                        u"созать новый."))

    def validate_date_unique(self):
        if not self.pk:
            _q1 = Q(start_date__gte=self.start_date, start_date__lte=self.end_date)
            _q2 = Q(end_date__gte=self.start_date, end_date__lte=self.end_date)
            _q3 = Q(start_date__lte=self.start_date, end_date__gte=self.end_date)
            if Semester.objects.filter(_q1 | _q2 | _q3):
                raise ValidationError(_(
                        u"Семестр пересекается с уже существующим."))

    def __unicode__(self):
        return u"%s - %s" % (
            dateformat(self.start_date, settings.DATE_FORMAT),
            dateformat(self.end_date, settings.DATE_FORMAT)
        )

    def clean(self):
        self.validate_date_end_gte_start()
        self.validate_date_edit()
        self.validate_date_unique()

    objects = SemesterManager()

    class Meta:
        verbose_name = _(u"семестр")
        verbose_name_plural = _(u"семестры")


class Group(models.Model):
    name = models.CharField(max_length=255, verbose_name=_(u"название"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u"группа")
        verbose_name_plural = _(u"группы")


class SubjectManager(ValidationManager):
    def filter_by_weekday(self, weekday, week=1, semester=None):
        if semester is None:
            semester = Semester.objects.get_current_semester()
        if weekday not in range(7):
            raise ValueError(u"weekday have to be in range 0..6")
        if week not in (1, 2):
            raise ValueError(u"week have to be 1 or 2")

        week1, week2, week3 = monthcalendar(
            semester.start_date.year, semester.start_date.month)[:3]
        if semester.starts_from_1st_week:
            _week1 = [w1 or w3 for w1, w3 in zip(week1, week3)]
            _week2 = week2
        else:
            _week1 = week2
            _week2 = [w1 or w3 for w1, w3 in zip(week1, week3)]
        week = (_week1, _week2)[week - 1]
        day_of_month = week[weekday]

        start_datetime = datetime(
            semester.start_date.year, semester.start_date.month, day_of_month)
        end_datetime = datetime.combine(start_datetime, time(23, 59))
        # TODO: May be do not query DB here
        subjects = Lesson.objects.filter(
            start_datetime__gte=start_datetime,
            start_datetime__lte=end_datetime
            ).values_list('subject__pk', flat=True)
        return self.filter(pk__in=subjects)

    def iter_by_weekdays(self, week=1, semester=None, limit=7):
        for weekday in range(limit):
            yield self.filter_by_weekday(
                weekday=weekday, week=week, semester=semester)


class Subject(models.Model):
    name = models.CharField(max_length=255, verbose_name=_(u"название"))
    group = models.ForeignKey(Group, verbose_name=_(u"группа"))
    semester = models.ForeignKey(Semester, verbose_name=_(u"семестр"), default=Semester.objects.get_current_semester)
    start_datetime = models.DateTimeField(verbose_name=_(u"дата и время первого занятия"), unique=True)
    per2weeks = models.BooleanField(default=False, verbose_name=_(u"раз в две недели"))

    def __unicode__(self):
        return u"%s | %s | %s | %s" % (
            self.name,
            self.group,
            dateformat(self.start_datetime, "l H:i"),
            dateformat(self.semester.start_date, "Y")
        )

    def get_lessons_datetimes(self):
        class_datetime = self.start_datetime
        end_datetime = datetime.combine(self.semester.end_date, time(23, 59))
        while class_datetime < end_datetime:
            yield class_datetime
            class_datetime += timedelta(7 + (0, 7)[self.per2weeks])

    #==========================================================================
    # Validation
    #==========================================================================
    def validate_semester(self):
        if self.pk:
            old_obj = Subject.objects.get(pk=self.pk)
            new_obj = self
            if old_obj.semester != new_obj.semester:
                raise ValidationError(_(
                        u"Вы не можете изменить семестр существующего "
                        u"предмета. Вы можете удалить существующий предмет и "
                        u"созать новый."))

    def validate_start_datetime_range(self):
        start_datetime = datetime.combine(self.semester.start_date, time())
        end_datetime = datetime.combine(self.semester.start_date, time(23, 59))
        end_datetime += timedelta(3 * 7)
        if not (start_datetime < self.start_datetime < end_datetime):
            raise ValidationError(_(
                u"Дата первого занятия должна быть не позже трех "
                u"недель от начала семестра."))

    def validate_start_datetime_edit(self):
        if self.pk:
            old_obj = Subject.objects.get(pk=self.pk)
            new_obj = self
            old_date = datetime.combine(old_obj.start_datetime, time())
            new_date = datetime.combine(new_obj.start_datetime, time())
            if old_date != new_date:
                raise ValidationError(_(
                        u"Вы не можете редактировать дату начала существующего "
                        u"предмета. Вы можете удалить существующий предмет и "
                        u"созать новый."))

    def validate_per2weeks(self):
        if self.pk:
            old_obj = Subject.objects.get(pk=self.pk)
            new_obj = self
            if old_obj.per2weeks != new_obj.per2weeks:
                raise ValidationError(_(
                        u'Вы не можете редактировать параметр "раз в две недели" '
                        u"существующего предмета. Вы можете удалить "
                        u"существующий предмет и созать новый."))

    def validate_datetime_unique(self):
        start_datetime = self.start_datetime
        end_datetime = self.start_datetime + timedelta(minutes=conf.LESSON_LENGTH)
        _q1 = Q(start_datetime__gte=start_datetime, start_datetime__lte=end_datetime)
        _q2 = Q(start_datetime__gte=start_datetime - timedelta(minutes=conf.LESSON_LENGTH),
                start_datetime__lte=start_datetime)
        if Lesson.objects.filter((_q1 | _q2) & ~Q(subject__pk=self.pk)):
            raise ValidationError(_(
                    u"Предмет пересекается по времени с уже существующим."))

    def clean(self):
        self.validate_semester()
        self.validate_start_datetime_range()
        self.validate_start_datetime_edit()
        self.validate_per2weeks()
        self.validate_datetime_unique()
    #--------------------------------------------------------------------------

    def _generate_lessons(self):
        lessons = Lesson.objects.filter(subject=self)
        for start_datetime, lesson in izip_longest(self.get_lessons_datetimes(), lessons):
            if not lesson:
                lesson = Lesson(subject=self)
            lesson.start_datetime = start_datetime
            lesson.save()

    def save(self, *args, **kwargs):
        super(Subject, self).save(*args, **kwargs)
        self._generate_lessons()

    objects = SubjectManager()

    class Meta:
        ordering = ["start_datetime"]
        verbose_name = _(u"предмет")
        verbose_name_plural = _(u"предметы")


class LessonManager(ValidationManager):
    pass


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, editable=False, verbose_name=_(u"предмет"))
    start_datetime = models.DateTimeField(editable=False, verbose_name=_(u"дата и время"))
    canceled = models.BooleanField(default=False, verbose_name=_(u"отменено"))

    def __unicode__(self):
        return u"%s | %s | %s" % (
            self.subject.name,
            self.subject.group.name,
            dateformat(self.start_datetime, settings.DATETIME_FORMAT)
        )

    def validate_start_datetime(self):
        if self.start_datetime not in self.subject.get_lessons_datetimes():
            raise ValidationError(_(u"Неправильные дата и время"))

    def clean(self):
        self.validate_start_datetime()

    objects = LessonManager()

    class Meta:
        ordering = ["start_datetime"]
        verbose_name = _(u"занятие")
        verbose_name_plural = _(u"занятия")
