from django.db import models


class ValidationManager(models.Manager):
    def create(self, **kwargs):
        obj = self.model(**kwargs)
        obj.full_clean()
        self._for_write = True
        obj.save(force_insert=True, using=self.db)
        return obj
