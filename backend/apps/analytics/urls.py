from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlertRecordViewSet, energy_overview, power_analysis

router = DefaultRouter()
router.register(r'alerts', AlertRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('overview/', energy_overview),
    path('power/', power_analysis),
]