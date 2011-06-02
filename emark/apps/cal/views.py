from itertools import izip_longest

from django.shortcuts import render_to_response
from django.template import RequestContext

from core.models import Lesson


def index(request, **kwargs):
    template_name = kwargs.pop('template_name', 'cal/base.haml')

    ctx = {"timetable": [
            list(izip_longest(w1, w2)) for w1, w2 in list(izip_longest(
                Lesson.objects.iter_by_weekdays(week=1),
                Lesson.objects.iter_by_weekdays(week=2)))
            ]
           }

    return render_to_response(
        template_name,
        ctx,
        RequestContext(request)
    )
