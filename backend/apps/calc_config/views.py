from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.calc_config.models import CalcTemplate, CalcBoundaryItem, CalcFactor
from apps.calc_config.serializers import CalcTemplateSerializer, CalcBoundaryItemSerializer, CalcFactorSerializer
from apps.common.pagination import StandardResultsSetPagination


class CalcTemplateViewSet(viewsets.ModelViewSet):
    """Provide CRUD endpoints for accounting templates."""
    queryset = CalcTemplate.objects.all()
    serializer_class = CalcTemplateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class CalcBoundaryItemViewSet(viewsets.ModelViewSet):
    """Provide CRUD endpoints for template boundary items."""
    queryset = CalcBoundaryItem.objects.all()
    serializer_class = CalcBoundaryItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class CalcFactorViewSet(viewsets.ModelViewSet):
    """Provide CRUD endpoints for factor management."""
    queryset = CalcFactor.objects.all()
    serializer_class = CalcFactorSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
