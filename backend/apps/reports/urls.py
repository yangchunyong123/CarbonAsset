from rest_framework.routers import DefaultRouter

from apps.reports.views import ReportRecordViewSet

router = DefaultRouter()
router.register("records", ReportRecordViewSet, basename="report-records")

urlpatterns = router.urls
