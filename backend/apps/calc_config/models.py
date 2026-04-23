from django.db import models


class CalcTemplate(models.Model):
    """Store accounting template metadata by industry."""
    name = models.CharField(max_length=128)
    industry = models.CharField(max_length=128)
    version = models.CharField(max_length=32, default="v1")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]


class CalcBoundaryItem(models.Model):
    """Store configurable boundary items under a template."""
    template = models.ForeignKey(CalcTemplate, on_delete=models.CASCADE, related_name="boundary_items")
    name = models.CharField(max_length=128)
    item_type = models.CharField(max_length=64, default="过程排放")
    formula = models.TextField(blank=True)
    factor_ref = models.CharField(max_length=128, blank=True)
    sort = models.IntegerField(default=0)
    is_enabled = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort", "id"]


class CalcFactor(models.Model):
    """Store factor values with version and effective date."""
    name = models.CharField(max_length=128)
    factor_type = models.CharField(max_length=64, default="排放因子")
    unit = models.CharField(max_length=32, blank=True)
    value = models.DecimalField(max_digits=16, decimal_places=6, default=0)
    version = models.CharField(max_length=32, default="v1")
    effective_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]
