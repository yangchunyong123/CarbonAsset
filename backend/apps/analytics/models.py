from django.db import models

class AlertRecord(models.Model):
    """Store system warnings and alerts."""
    LEVEL_CHOICES = (
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    )
    title = models.CharField(max_length=128)
    content = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='warning')
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
