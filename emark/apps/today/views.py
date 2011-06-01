from django.shortcuts import render_to_response
from django.template import RequestContext

from today.models import TodayLesson


def index(request, **kwargs):
    template_name = kwargs.pop('template_name', 'today/base.haml')

    object_list = TodayLesson.objects.all()
    return render_to_response(
        template_name,
        RequestContext(request, {'object_list': object_list})
    )

def detail(request, **kwargs):
    template_name = kwargs.pop('template_name', 'today/base.haml')

    object_list = TodayLesson.objects.all()
    return render_to_response(
        template_name,
        RequestContext(request, {'object_list': object_list})
    )
