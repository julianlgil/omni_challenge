from django.db import models
from common.models import BaseModel
from orders.models import Orders
from .constants import SHIPMENT_STATUS


class Shipments(BaseModel):
    address = models.CharField(max_length=100)
    order = models.ForeignKey(to=Orders, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=30, choices=SHIPMENT_STATUS)

    class Meta:
        db_table = "shipments"
