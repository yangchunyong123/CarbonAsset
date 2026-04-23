from rest_framework.routers import DefaultRouter

from apps.calculation.views import CalcTaskViewSet

router = DefaultRouter()
router.register("tasks", CalcTaskViewSet, basename="calc-tasks")

urlpatterns = router.urls
