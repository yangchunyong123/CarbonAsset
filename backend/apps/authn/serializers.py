from django.contrib.auth.models import User
from rest_framework import serializers

from apps.authn.models import Menu


class LoginSerializer(serializers.Serializer):
    """Validate login payload."""
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """Serialize minimal user info for current session."""

    class Meta:
        model = User
        fields = ["id", "username", "is_staff", "is_superuser"]


class MenuSerializer(serializers.ModelSerializer):
    """Serialize menu tree nodes."""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ["id", "name", "path", "component", "sort", "children"]

    def get_children(self, obj):
        """Return nested children menus in order."""
        return MenuSerializer(obj.children.order_by("sort", "id"), many=True).data
