from django.shortcuts import render_to_response
from django.template import RequestContext

from cal.models import Calendar


def index(request, **kwargs):
    template_name = kwargs.pop('template_name', 'cal/base.haml')

    return render_to_response(
        template_name,
        {"week": Calendar().iter_by_weekdays()},
        RequestContext(request)
    )
