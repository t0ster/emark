from django.contrib import admin
from django.contrib.admin.sites import AdminSite

import core
import core.admin

site = AdminSite("settings")  # pylint: disable-msg=C0103
site.index_template = "settings/index.html"
site.app_index_template = "settings/app_index.html"

site.register((
    core.models.Semester,
    core.models.Group,
))
site.register(core.models.Subject, core.admin.SubjectAdmin)
# site.register(core.models.Lesson, LessonAdmin)
