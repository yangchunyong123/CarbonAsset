from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.common.pagination import StandardResultsSetPagination
from apps.reports.models import ReportRecord
from apps.reports.serializers import ReportRecordSerializer


class ReportRecordViewSet(viewsets.ModelViewSet):
    """Provide report management APIs including download endpoint."""
    queryset = ReportRecord.objects.prefetch_related("attachments").all()
    serializer_class = ReportRecordSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        """Return a text report file for quick local verification."""
        report = self.get_object()
        content = (
            f"报告名称: {report.name}\n类型: {report.get_report_type_display()}\n"
            f"年份: {report.year}\n月份: {report.month}"
        )
        response = HttpResponse(content, content_type="text/plain; charset=utf-8")
        response["Content-Disposition"] = f"attachment; filename=report_{report.id}.txt"
        return response
