from django.db import models
from django.urls import reverse

from django.template.defaultfilters import slugify

class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    last_conn = models.DateTimeField(default=None, blank=True, null=True)

    class Meta:
        abstract = True


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
    
    def __str__(self):
        return self.name


class Registry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.CharField(max_length=100)
    quantity = models.IntegerField()

    class Meta:
        abstract = True


class Transaction(Registry):
    supplier = models.ForeignKey(CD, on_delete=models.CASCADE, related_name='sales') 
    buyer = models.ForeignKey(CD, on_delete=models.CASCADE, related_name='purchases')
    total = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} | Sale: {self.supplier} - Purchase: {self.buyer} | Total: {self.total}"


class Order(Registry):
    STATUS_CHOICES = (
        ('pendent', 'Pendent'),
        ('complete', 'Complete'),
        ('failed', 'Failed')
    )

    client = models.ForeignKey(CD, related_name='ordered_supplies', on_delete=models.CASCADE)
    seller = models.ForeignKey(CD, related_name='ordered_sales', on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, editable=False)

    def __str__(self):
        return f"Order ({self.created_at}): {self.client} - {self.seller}"
    