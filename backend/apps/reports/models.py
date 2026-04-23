from django.db import models


class ReportRecord(models.Model):
    """Store generated report metadata and summarized values."""
    REPORT_CHOICES = [
        ("emission", "排放报告"),
        ("energy", "能耗报告"),
        ("warning", "告警报告"),
    ]
    name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=32, choices=REPORT_CHOICES, default="emission")
    year = models.IntegerField()
    month = models.IntegerField(default=1)
    total_emission = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    total_energy = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    value_added = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    file_path = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=32, default="generated")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]


class ReportAttachment(models.Model):
    """Store report attachment records for download."""
    report = models.ForeignKey(ReportRecord, on_delete=models.CASCADE, related_name="attachments")
    file_name = models.CharField(max_length=255)
    file_url = models.CharField(max_length=255)
