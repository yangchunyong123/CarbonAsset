from rest_framework.routers import DefaultRouter

from apps.master_data.views import FuelTypeViewSet, MaterialViewSet

router = DefaultRouter()
router.register("fuels", FuelTypeViewSet, basename="fuels")
router.register("materials", MaterialViewSet, basename="materials")

urlpatterns = router.urls
