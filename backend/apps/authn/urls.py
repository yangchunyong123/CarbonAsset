from django.urls import path

from apps.authn.views import login_view, me_view, menus_view, bootstrap_admin

urlpatterns = [
    path("login", login_view),
    path("me", me_view),
    path("menus", menus_view),
    path("bootstrap-admin", bootstrap_admin),
]
