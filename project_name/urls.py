from django.contrib import admin
from django.urls import path, include

from {{ project_name }}.views import (
    home,
    handle_error_401,
    handle_error_403,
    handle_error_404,
    handle_error_500,
)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
]

handler401 = handle_error_401
handler403 = handle_error_403
handler404 = handle_error_404
handler500 = handle_error_500

