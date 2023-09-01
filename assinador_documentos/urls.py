from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

from users.views import index

urlpatterns = [
    path("", index, name="index"),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("accounts/logout/", LogoutView.as_view(next_page="index"), name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
]
