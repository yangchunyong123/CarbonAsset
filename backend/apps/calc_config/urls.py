from rest_framework.routers import DefaultRouter

from apps.calc_config.views import CalcTemplateViewSet, CalcBoundaryItemViewSet, CalcFactorViewSet

router = DefaultRouter()
router.register("templates", CalcTemplateViewSet, basename="calc-templates")
router.register("boundary-items", CalcBoundaryItemViewSet, basename="boundary-items")
router.register("factors", CalcFactorViewSet, basename="factors")

urlpatterns = router.urls
