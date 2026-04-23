from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.authn.urls")),
    path("api/v1/auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/master-data/", include("apps.master_data.urls")),
    path("api/v1/calc-config/", include("apps.calc_config.urls")),
    path("api/v1/data-entry/", include("apps.data_entry.urls")),
    path("api/v1/calculation/", include("apps.calculation.urls")),
    path("api/v1/reports/", include("apps.reports.urls")),
    path("api/v1/analytics/", include("apps.analytics.urls")),
]
