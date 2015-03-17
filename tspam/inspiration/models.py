from django.db import models
from django.utils.timezone import now

class Timestamps(models.Model):
    created = models.DateTimeField(blank=True)
    modified = models.DateTimeField(blank=True)

    def save(self, *args, **kw):
        if not self.id:
            if not self.created:
                self.created = now()
        self.modified = now()
        super(Timestamps, self).save(*args, **kw)

    class Meta:
        abstract = True

class Product(models.Model):
    color = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)
    source_url = models.CharField(max_length=255, null=True, blank=True)