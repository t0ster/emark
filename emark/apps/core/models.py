# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, date, time

from django.db import models
from django.conf import settings
from django.utils.dateformat import format as dateformat
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


_(u"core")
_(u"Core")


class SemesterManager(models.Manager):
    def get_current_semester(self):
        today = date.today()
        try:
            return self.get(start_date__lte=today, end_date__gte=today)
        except Semester.DoesNotExist:
            return None


class Semester(models.Model):
    start_date = models.DateField(verbose_name=_(u"дата начала"))
    end_date = models.DateField(verbose_name=_(u"дата конца"))

    def __unicode__(self):
        return "%s - %s" % (
            dateformat(self.start_date, settings.DATE_FORMAT),
            dateformat(self.end_date, settings.DATE_FORMAT)
        )

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


class Subject(models.Model):
    name = models.CharField(max_length=255, verbose_name=_(u"название"))
    group = models.ForeignKey(Group, verbose_name=_(u"группа"))
    semester = models.ForeignKey(Semester, verbose_name=_(u"семестр"), default=Semester.objects.get_current_semester)
    start_datetime = models.DateTimeField(verbose_name=_(u"дата и время первого занятия"))
    per2weeks = models.BooleanField(default=False, verbose_name=_(u"раз в две недели"))

    def __unicode__(self):
        return "%s | %s" % (
            self.name,
            dateformat(self.semester.start_date, "Y")
        )

    def get_lessons_datetimes(self):
        class_datetime = self.start_datetime
        end_datetime = datetime.combine(self.semester.end_date, time(23, 59))
        while class_datetime < end_datetime:
            yield class_datetime
            class_datetime += timedelta(7 + (0, 7)[self.per2weeks])

    def validate_semester(self):
        if self.pk:
            old_obj = Subject.objects.get(pk=self.pk)
            new_obj = self
            if old_obj.semester != new_obj.semester:
                raise ValidationError(_(
                        u"Вы не можете изменить семестр существующего "
                        u"предмета. Вы можете удалить существующий предмет и "
                        u"созать новый."))

    def validate_start_datetime_semester(self):
        start_datetime = datetime.combine(self.semester.start_date, time())
        end_datetime = datetime.combine(self.semester.end_date, time(23, 59))
        if not (start_datetime < self.start_datetime < end_datetime):
            raise ValidationError(_(
                u"Дата и время первого занятия должны быть между "
                u"началом и концом семестра"))

    def validate_start_datetime_date(self):
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
                        u"Вы не можете редактировать параметр раз в две недели "
                        u"существующего предмета. Вы можете удалить "
                        u"существующий предмет и созать новый."))

    def _generate_lessons(self):
        lessons = Lesson.objects.filter(subject=self)
        if not lessons:
            lessons = [None] * len(list(self.get_lessons_datetimes()))
        for start_datetime, lesson in zip(self.get_lessons_datetimes(), lessons):
            if not lesson:
                lesson = Lesson(subject=self)
            lesson.start_datetime = start_datetime
            lesson.save()

    def clean(self):
        self.validate_semester()
        self.validate_start_datetime_semester()
        self.validate_start_datetime_date()
        self.validate_per2weeks()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Subject, self).save(*args, **kwargs)
        self._generate_lessons()

    class Meta:
        verbose_name = _(u"предмет")
        verbose_name_plural = _(u"предметы")


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, editable=False, verbose_name=_(u"предмет"))
    start_datetime = models.DateTimeField(editable=False, verbose_name=_(u"дата и время"))
    canceled = models.BooleanField(default=False, verbose_name=_(u"отменено"))

    def __unicode__(self):
        return "%s | %s | %s" % (
            self.subject.name,
            self.subject.group.name,
            dateformat(self.start_datetime, settings.DATETIME_FORMAT)
        )

    def validate_start_datetime(self):
        if self.start_datetime not in self.subject.get_lessons_datetimes():
            raise ValidationError(_(u"Неправильные дата и время"))

    def clean(self):
        self.validate_start_datetime()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Lesson, self).save(*args, **kwargs)

    class Meta:
        ordering = ["start_datetime"]
        verbose_name = _(u"занятие")
        verbose_name_plural = _(u"занятия")
