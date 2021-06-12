from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from common.models import BaseModel
from orders.constants import PENDING_PAYMENT, PENDING_SHIPPING
from orders.models import Orders
from .constants import PAYMENT_STATUS, PENDING, SUCCESSFUL


class Payment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    amount = models.FloatField()
    status = models.CharField(max_length=30, choices=PAYMENT_STATUS)

    class Meta:
        db_table = "payments"

    def set_payment_detail(self, order):
        return PaymentDetail.objects.create(payment=self, order=order)


class PaymentDetail(BaseModel):
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name="payment_detail")
    order = models.ForeignKey(Orders, on_delete=models.PROTECT)

    class Meta:
        db_table = "payment_details"
        unique_together = (("payment", "order"),)


@receiver(post_save, sender=Payment)
def my_handler(sender, **kwargs):
    payment = kwargs["instance"]
    payment_details = payment.payment_detail.all()
    for payment_detail in payment_details:
        order = payment_detail.order
        if payment.status == PENDING:
            order.balance -= payment.amount
            order.status = PENDING_PAYMENT
        if payment.status == SUCCESSFUL and order.balance == 0:
            order.status = PENDING_SHIPPING
        else:
            order.status = PENDING_PAYMENT
        order.save()
