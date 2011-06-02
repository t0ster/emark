from django.contrib import admin
from django.contrib.admin.sites import AdminSite

import core

site = AdminSite("settings")  # pylint: disable-msg=C0103
site.index_template = "settings/index.html"
site.app_index_template = "settings/app_index.html"


class LessonAdmin(admin.ModelAdmin):
    list_filter = ("subject", "subject__group", "subject__semester")

site.register((
    core.models.Semester,
    core.models.Group,
    core.models.Subject,
))
# site.register(core.models.Lesson, LessonAdmin)
