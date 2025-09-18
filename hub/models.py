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
        return reverse("cd_detail_slug", kwargs={"slug": self.slug})
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Transaction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    supplier = models.ForeignKey(CD, related_name='sales', on_delete=models.CASCADE) 
    buyer = models.ForeignKey(CD, related_name='purchases', on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    quantity = models.IntegerField()
    total = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} | Sale: {self.supplier} - Purchase: {self.buyer} | Total: {self.total}"
