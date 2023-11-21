from django.db import models
from django.db.models import Sum
# Create your models here.

from django.contrib.auth.models import AbstractUser

class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
class CustomUser(AbstractUser,BaseModel):
    
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    name = models.CharField(max_length=15, blank=True, null=True)
    simplify = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Ledger(BaseModel):

    SPLIT_CHOICES = [
        ('PERCENT', 'PERCENT'),
        ('EQUAL', 'EQUAL'),
        ('EXACT', 'EXACT'),
    ]
    total_amount = models.FloatField(default=0)
    note = models.CharField(max_length=200,default=None,null=True)
    split_with = models.JSONField(default=None,null=True)
    split_type = models.CharField(max_length=200,default=None,null=True, choices=SPLIT_CHOICES)

class Own(BaseModel):
    Debtor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='debtor')
    Creditor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='creditor')
    amount = models.FloatField(default=0)
    
    @property
    def simplified_amount(self):
       

        user_records_given = Own.objects.filter(Creditor=self.Creditor).aggregate(total_amount=Sum('amount'))['total_amount'] 

        user_records_taken = Own.objects.filter(Debtor=self.Creditor).aggregate(total_amount=Sum('amount'))['total_amount']

        user_records_given = user_records_given if user_records_given else 0
        user_records_taken = user_records_taken if user_records_taken else 0
        return user_records_given - user_records_taken 







   
