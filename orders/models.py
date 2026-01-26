from django.db import models
from django.urls import reverse
import uuid

from hub.models import CD

class Order(models.Model):
    PENDING = 'pdg'
    CONFIRMED = 'cnf'
    IN_QUEUE = 'iqu'
    AWAITING_CUSTOMER_DECISION = 'acd'
    IN_PROGRESS = 'ipr'
    COMPLETED = 'cmp'
    REJECTED = 'rej'

    ORDER_STATUS_CHOICES = (
    (PENDING, 'Pending'),
    (CONFIRMED, 'Confirmed'),
    (IN_QUEUE, 'In Queue'),
    (AWAITING_CUSTOMER_DECISION, 'Awaiting Customer Decision'),
    (IN_PROGRESS, 'In Progress'),
    (COMPLETED, 'Completed'),
    (REJECTED, 'Rejected'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=3, choices=ORDER_STATUS_CHOICES, default=PENDING)
    client = models.ForeignKey(CD, related_name='orders', on_delete=models.CASCADE)
    sku = models.CharField(max_length=7)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, editable=False)

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"id": self.id})