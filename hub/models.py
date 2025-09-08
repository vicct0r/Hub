from django.db import models
from django.urls import reverse

from django.template.defaultfilters import slugify

class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    last_conn = models.DateTimeField(default=None, blank=True, null=True)


class CD(Base):
    name = models.CharField(max_length=90, unique=True)
    description = models.TextField(blank=True, null=True)
    ip = models.CharField(max_length=120)
    balance = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    region = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(null=True)

    def get_absolute_url(self):
        return reverse("cd_detail", kwargs={"slug": self.slug})
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)