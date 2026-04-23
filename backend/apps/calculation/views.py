from decimal import Decimal

from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.calculation.models import CalcTask, CalcResult, CalcResultDetail
from apps.calculation.serializers import CalcTaskSerializer
from apps.common.pagination import StandardResultsSetPagination
from apps.data_entry.models import EntryMonthlyData


class CalcTaskViewSet(viewsets.ModelViewSet):
    """Provide task management and execution endpoint for calculations."""
    queryset = CalcTask.objects.select_related("result", "entry").all()
    serializer_class = CalcTaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    @action(detail=False, methods=["post"])
    def run(self, request):
        """Execute a simplified calculation task from an entry ID."""
        entry_id = request.data.get("entry_id")
        if not entry_id:
            return Response({"code": 40001, "message": "entry_id 不能为空", "data": {}}, status=status.HTTP_400_BAD_REQUEST)
        try:
            entry = EntryMonthlyData.objects.prefetch_related("items").get(id=entry_id)
        except EntryMonthlyData.DoesNotExist:
            return Response({"code": 40004, "message": "填报数据不存在", "data": {}}, status=status.HTTP_404_NOT_FOUND)
        task = CalcTask.objects.create(entry=entry, status="running", started_at=timezone.now())
        total_energy = sum([item.value for item in entry.items.all()])
        total_emission = Decimal(total_energy) * Decimal("2.35")
        intensity = Decimal("0") if total_energy == 0 else total_emission / Decimal(total_energy)
        result = CalcResult.objects.create(
            task=task,
            total_emission=total_emission,
            total_energy=total_energy,
            intensity=intensity,
            yoy=Decimal("0.12"),
        )
        CalcResultDetail.objects.bulk_create(
            [
                CalcResultDetail(result=result, metric_name="总能耗", metric_value=total_energy, unit="吨标煤"),
                CalcResultDetail(result=result, metric_name="总排放", metric_value=total_emission, unit="吨CO2"),
            ]
        )
        task.status = "success"
        task.message = "计算成功"
        task.ended_at = timezone.now()
        task.save(update_fields=["status", "message", "ended_at"])
        serializer = self.get_serializer(task)
        return Response({"code": 0, "message": "ok", "data": serializer.data})
