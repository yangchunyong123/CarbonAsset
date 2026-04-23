from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.common.pagination import StandardResultsSetPagination
from apps.master_data.models import FuelType, Material
from apps.master_data.serializers import FuelTypeSerializer, MaterialSerializer


class FuelTypeViewSet(viewsets.ModelViewSet):
    """Provide CRUD endpoints for fuel types."""
    queryset = FuelType.objects.all()
    serializer_class = FuelTypeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class MaterialViewSet(viewsets.ModelViewSet):
    """Provide CRUD endpoints for production materials."""
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
