from django.db import models

class Product(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField( max_length=100)
    description = models.CharField(max_length=250 )
    price = models.DecimalField(max_digits=10 ,decimal_places=2 )
    is_available = models.BooleanField(default=True)

def __str__(self):
    return f"{self.external_id}: {self.name} (${self.price})"
