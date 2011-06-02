from datetime import datetime, time

from django.db import models

from core.models import Lesson


class TodayLessonManager(models.Manager):
    def get_query_set(self, *args, **kwargs):
        now = datetime.now()
        end_of_the_day = datetime.combine(now, time(23, 59))
        return super(TodayLessonManager, self).get_query_set(
            *args, **kwargs).filter(
            start_datetime__gte=now, start_datetime__lte=end_of_the_day)


class TodayLesson(Lesson):
    @models.permalink
    def get_absolute_url(self):
        return ("lesson_detail", (), {
            "pk": self.pk
        })

    objects = TodayLessonManager()

    class Meta:
        proxy = True
