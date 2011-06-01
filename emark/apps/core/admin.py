from django.contrib import admin
from core import models


class LessonAdmin(admin.ModelAdmin):
    list_filter = ("subject", "subject__group", "subject__semester")

admin.site.register(models.Semester)
admin.site.register(models.Group)
admin.site.register(models.Subject)
admin.site.register(models.Lesson, LessonAdmin)
