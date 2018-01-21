from django.db import models
from django.contrib.auth import get_user_model
from django.db import models

from bills.models import Bill

User = get_user_model()


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    date_paid = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    status = models.CharField(max_length=8,default='NOT PAID')
    additional_notes = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=False, blank=False, related_name='payments')

    def __str__(self):
        return '{}: {}'.format(self.bill, self.id)
