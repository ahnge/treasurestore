from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Treasure Store Administration"
admin.site.site_title = "Treasure Store"
admin.site.index_title = "Welcome to Treasure Store Administration"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("store.urls")),
]
