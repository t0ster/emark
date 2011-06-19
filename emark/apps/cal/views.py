from django.shortcuts import render_to_response
from django.template import RequestContext

from cal.utils import Calendar
from core.models import Semester


def index(request, **kwargs):
    template_name = kwargs.pop('template_name', 'cal/base.haml')
    try:
        ctx = {"week": Calendar().iter_by_weekdays()}
    except Semester.DoesNotExist:
        ctx = {"week": None}

    return render_to_response(
        template_name,
        ctx,
        RequestContext(request)
    )
