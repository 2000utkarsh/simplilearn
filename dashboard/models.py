from django.db import models

# Create your models here.

class OrderID(models.Model):
    order_id = models.CharField(max_length= 40, default=None, blank=True, null = True)

    def __str__(self):
        return f'{self.order_id}'
