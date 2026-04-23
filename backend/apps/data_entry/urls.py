from rest_framework.routers import DefaultRouter

from apps.data_entry.views import EntryMonthlyDataViewSet

router = DefaultRouter()
router.register("entries", EntryMonthlyDataViewSet, basename="entries")

urlpatterns = router.urls
