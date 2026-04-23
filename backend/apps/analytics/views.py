from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import AlertRecord
from .serializers import AlertRecordSerializer
from apps.common.response import ok

class AlertRecordViewSet(viewsets.ModelViewSet):
    queryset = AlertRecord.objects.all()
    serializer_class = AlertRecordSerializer

@api_view(['GET'])
def energy_overview(request):
    """Mock aggregation for energy and carbon overview."""
    data = {
        "total_carbon": 12500.5,
        "total_energy": 45000.0,
        "trend_data": {
            "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "carbon": [1000, 1200, 1100, 1300, 1500, 1400],
            "energy": [3000, 3200, 3100, 3500, 3800, 3600]
        }
    }
    return ok(data)

@api_view(['GET'])
def power_analysis(request):
    """Mock aggregation for power analysis."""
    data = {
        "total_power": 8500.0,
        "peak_valley": [
            {"name": "Peak", "value": 3000},
            {"name": "Flat", "value": 4000},
            {"name": "Valley", "value": 1500}
        ]
    }
    return ok(data)
