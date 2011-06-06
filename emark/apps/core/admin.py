from django.contrib import admin
from core import models


class LessonAdmin(admin.ModelAdmin):
    list_filter = ("subject", "subject__group", "subject__semester")


class SubjectAdmin(admin.ModelAdmin):
    list_filter = ("semester", "group")

admin.site.register((
    models.Semester,
    models.Group,
))
admin.site.register(models.Subject, SubjectAdmin)
# admin.site.register(models.Lesson, LessonAdmin)
