from django.conf import settings
from django.db import models


class EntryMonthlyData(models.Model):
    """Store monthly submission header records."""
    STATUS_CHOICES = [
        ("draft", "草稿"),
        ("submitted", "已提交"),
    ]

    year = models.IntegerField()
    month = models.IntegerField()
    org_name = models.CharField(max_length=255)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="draft")
    remark = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-year", "-month", "-id"]


class EntryMonthlyItem(models.Model):
    """Store monthly submission detail line items."""
    entry = models.ForeignKey(EntryMonthlyData, on_delete=models.CASCADE, related_name="items")
    energy_type = models.CharField(max_length=64)
    sub_type = models.CharField(max_length=128, blank=True)
    value = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    cost = models.DecimalField(max_digits=16, decimal_places=4, default=0)
