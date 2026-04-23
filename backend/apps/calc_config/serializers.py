from rest_framework import serializers

from apps.calc_config.models import CalcTemplate, CalcBoundaryItem, CalcFactor


class CalcBoundaryItemSerializer(serializers.ModelSerializer):
    """Serialize template boundary item records."""

    class Meta:
        model = CalcBoundaryItem
        fields = "__all__"


class CalcTemplateSerializer(serializers.ModelSerializer):
    """Serialize templates and nested boundary items."""
    boundary_items = CalcBoundaryItemSerializer(many=True, read_only=True)

    class Meta:
        model = CalcTemplate
        fields = "__all__"


class CalcFactorSerializer(serializers.ModelSerializer):
    """Serialize factor records."""

    class Meta:
        model = CalcFactor
        fields = "__all__"
