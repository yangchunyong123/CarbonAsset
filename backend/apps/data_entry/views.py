from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.common.pagination import StandardResultsSetPagination
from apps.data_entry.models import EntryMonthlyData
from apps.data_entry.serializers import EntryMonthlyDataSerializer


class EntryMonthlyDataViewSet(viewsets.ModelViewSet):
    """Provide CRUD endpoints for monthly data submissions."""
    queryset = EntryMonthlyData.objects.prefetch_related("items").all()
    serializer_class = EntryMonthlyDataSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        """Persist creator for traceability when creating records."""
        serializer.save(created_by=self.request.user)
