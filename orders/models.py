from django.db import models
from django.urls import reverse
import uuid

from hub.models import CD

class Order(models.Model):
    PENDING = 'pdg'
    SCHEDULED = 'sch'
    IN_QUEUE = 'iqu'
    COMPLETED = 'cmp'
    DENIED = 'dnd'
    ACTIVE = 'act'

    ORDER_STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (SCHEDULED, 'Scheduled'),
        (IN_QUEUE, 'In Queue'),
        (COMPLETED, 'Completed'),
        (DENIED, 'Denied'),
        (ACTIVE, 'Active')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=3, choices=ORDER_STATUS_CHOICES, default=PENDING)
    client = models.ForeignKey(CD, related_name='orders', on_delete=models.SET_NULL, null=True)
    product = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"id": self.id})