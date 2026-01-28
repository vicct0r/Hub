from django.db import models
from django.urls import reverse
import uuid
from django.core.exceptions import ValidationError

from hub.models import CD


class Order(models.Model):
    PENDING = 'pdg'
    CONFIRMED = 'cnf'
    IN_QUEUE = 'iqu'
    AWAITING_CUSTOMER_DECISION = 'acd'
    ON_ROUTE = 'ort'
    COMPLETED = 'cmp'
    REJECTED = 'rej'

    ORDER_STATUS_CHOICES = (
    (PENDING, 'Pending'),
    (CONFIRMED, 'Confirmed'),
    (IN_QUEUE, 'In Queue'),
    (AWAITING_CUSTOMER_DECISION, 'Awaiting Customer Decision'),
    (ON_ROUTE, 'On Route'),
    (COMPLETED, 'Completed'),
    (REJECTED, 'Rejected'),
    )

    CONFIRMED_CURRENT_BATCH_QUANTITY = 0
    WAITED_FOR_REQUESTED_BATCH_QUANTITY = 1

    ORDER_OPERATIONAL_CHOICES = (
        (CONFIRMED_CURRENT_BATCH_QUANTITY, 'Confirm Current Batch Quantity'),
        (WAITED_FOR_REQUESTED_BATCH_QUANTITY, 'Wait For Requested Batch Quantity')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=3, choices=ORDER_STATUS_CHOICES, default=PENDING)
    client = models.ForeignKey(CD, related_name='orders', on_delete=models.CASCADE)
    sku = models.CharField(max_length=7)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, editable=False)
    operation = models.SmallIntegerField(choices=ORDER_OPERATIONAL_CHOICES, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"id": self.id})
    
    def clean(self):
        if self.status == self.AWAITING_CUSTOMER_DECISION:
            if self.operation is None:
                raise ValidationError({
                    "operation": "A customer decision is required."
                })
        else:
            if self.operation is not None:
                raise ValidationError({
                    "operation": "This operation is only valid when waiting customer decision."
                })