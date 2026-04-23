from rest_framework import serializers

from apps.calculation.models import CalcTask, CalcResult, CalcResultDetail


class CalcResultDetailSerializer(serializers.ModelSerializer):
    """Serialize detailed metrics for a result."""

    class Meta:
        model = CalcResultDetail
        fields = "__all__"


class CalcResultSerializer(serializers.ModelSerializer):
    """Serialize calculation summary with detail metrics."""
    details = CalcResultDetailSerializer(many=True, read_only=True)

    class Meta:
        model = CalcResult
        fields = "__all__"


class CalcTaskSerializer(serializers.ModelSerializer):
    """Serialize calculation tasks and optional result."""
    result = CalcResultSerializer(read_only=True)

    class Meta:
        model = CalcTask
        fields = "__all__"
