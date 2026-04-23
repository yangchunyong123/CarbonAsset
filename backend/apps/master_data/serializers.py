from rest_framework import serializers

from apps.master_data.models import FuelType, Material


class FuelTypeSerializer(serializers.ModelSerializer):
    """Serialize fuel type records."""

    class Meta:
        model = FuelType
        fields = "__all__"


class MaterialSerializer(serializers.ModelSerializer):
    """Serialize material records."""

    class Meta:
        model = Material
        fields = "__all__"
