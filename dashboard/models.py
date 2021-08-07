from django.db import models
from accounts.models import User
# Create your models here.

class OrderID(models.Model):
    order_id = models.CharField(max_length= 40, default=None, blank=True, null = True)

    def __str__(self):
        return f'{self.order_id}'

class CardDetails(models.Model):
    
    CARD_CHOICES = [('CREDIT', 'CREDIT'), ('DEBIT', 'DEBIT')]
    username = models.ForeignKey(User, on_delete = models.CASCADE)
    name_on_card =  models.CharField(max_length= 40, default=None, blank=False, null = True) 
    card_bank =  models.CharField(max_length= 40, default=None, blank=False, null = True) 
    card_number =  models.CharField(max_length= 40, default=None, blank=False, null = True) 
    expiry_month =  models.CharField(max_length= 40, default=None, blank=False, null = True)
    expiry_year =  models.CharField(max_length= 40, default=None, blank=False, null = True)
    card_type = models.CharField(max_length=200, default=None, choices= CARD_CHOICES)
    

    def __str__(self):
        return f'{self.username} - {self.card_number}'

class BoughtCourses(models.Model):
    username = models.ForeignKey(User, on_delete = models.CASCADE)
    ids = models.CharField(max_length=100)
    