from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class NetworkNode(models.Model):
    """Model representing a network node."""
    name = models.CharField(max_length=50)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=50)
    debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    supplier = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def clean(self):
        "Validates that a supplier is not a descendant of the current node."
        if self.supplier:
            supplier = self.supplier
            while supplier:
                if supplier == self:
                    raise ValidationError("It is not possible to set yourself or one of your children as a supplier.")
                supplier = supplier.supplier
        super().clean()

    def save(self, *args, **kwargs):
        "Overrides save to call clean() for validation before saving."
        self.clean()
        super().save(*args, **kwargs)


class Product(models.Model):
    """Model representing a product."""
    name = models.CharField(max_length=25)
    model = models.CharField(max_length=100)
    release_date = models.DateField()
    network_node = models.ForeignKey(NetworkNode, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.model})"
    
    def clean(self):
        "Validates that the release date is not set in the future."
        if self.release_date > timezone.now().date():
            raise ValidationError("Release date cannot be in the future.")
        
    def save(self, *args, **kwargs):
        "Overrides save to call clean() for validation before saving."
        self.clean()
        super().save(*args, **kwargs)


class Employee(models.Model):
    """Model representing a employee."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    network_node = models.ForeignKey(NetworkNode, related_name='employees', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
