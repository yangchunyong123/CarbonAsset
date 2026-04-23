from django.conf import settings
from django.db import models


class Role(models.Model):
    """Store role definitions for RBAC."""
    code = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        """Return role display name."""
        return self.name


class Menu(models.Model):
    """Store navigable menu items and route definitions."""
    name = models.CharField(max_length=128)
    path = models.CharField(max_length=256)
    component = models.CharField(max_length=256, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="children")
    sort = models.IntegerField(default=0)

    class Meta:
        ordering = ["sort", "id"]


class UserRole(models.Model):
    """Map user to role."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "role")


class RoleMenu(models.Model):
    """Map role to menu."""
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("role", "menu")
