from django.db import models


class FuelType(models.Model):
    """Store fuel type master data and factor settings."""
    name = models.CharField(max_length=128, unique=True)
    category = models.CharField(max_length=64, default="化石燃料")
    form = models.CharField(max_length=64, default="固态")
    alias = models.CharField(max_length=128, blank=True)
    carbon_content = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    oxidation_rate = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    emission_factor = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]


class Material(models.Model):
    """Store production material and process links for accounting."""
    name = models.CharField(max_length=128, unique=True)
    process_link = models.CharField(max_length=255, blank=True)
    emission_factor = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]
