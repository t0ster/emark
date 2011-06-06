from django.conf import settings

LESSON_LENGTH = getattr(settings, "LESSON_LENGTH", 90)
