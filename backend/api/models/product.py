from django.db import models 

class Product(models.Model):
    name = models.CharField(max_length=500)
    serial = models.CharField(max_length=250, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.id} {self.name}"