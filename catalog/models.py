from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
import uuid


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    name = models.CharField(unique=True, max_length=200)
    sku = models.CharField(unique=True, max_length=7)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.sku
    
    def get_absolute_path(self):
        return reverse('catalog:slug_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)