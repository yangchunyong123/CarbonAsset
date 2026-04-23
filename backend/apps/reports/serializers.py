from rest_framework import serializers

from apps.reports.models import ReportRecord, ReportAttachment


class ReportAttachmentSerializer(serializers.ModelSerializer):
    """Serialize report attachments."""

    class Meta:
        model = ReportAttachment
        fields = "__all__"


class ReportRecordSerializer(serializers.ModelSerializer):
    """Serialize reports and attachment list."""
    attachments = ReportAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = ReportRecord
        fields = "__all__"
