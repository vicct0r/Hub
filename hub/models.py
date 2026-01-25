from django.db import models
from django.urls import reverse

from django.template.defaultfilters import slugify
import uuid

class CD(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=90, unique=True, blank=True, null=True)
    ip = models.CharField(max_length=120, unique=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(null=True)

    def get_absolute_url(self):
        return reverse("cd_detail_slug", kwargs={"slug": self.slug})
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)