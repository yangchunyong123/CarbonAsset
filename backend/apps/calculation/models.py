from django.db import models

from apps.data_entry.models import EntryMonthlyData


class CalcTask(models.Model):
    """Store execution status of accounting calculation jobs."""
    STATUS_CHOICES = [
        ("pending", "待执行"),
        ("running", "执行中"),
        ("success", "成功"),
        ("failed", "失败"),
    ]

    entry = models.ForeignKey(EntryMonthlyData, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="pending")
    message = models.CharField(max_length=255, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]


class CalcResult(models.Model):
    """Store calculation summary metrics."""
    task = models.OneToOneField(CalcTask, on_delete=models.CASCADE, related_name="result")
    total_emission = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    total_energy = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    intensity = models.DecimalField(max_digits=16, decimal_places=6, default=0)
    yoy = models.DecimalField(max_digits=8, decimal_places=4, default=0)


class CalcResultDetail(models.Model):
    """Store calculation detail rows for display and export."""
    result = models.ForeignKey(CalcResult, on_delete=models.CASCADE, related_name="details")
    metric_name = models.CharField(max_length=128)
    metric_value = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    unit = models.CharField(max_length=32, blank=True)
