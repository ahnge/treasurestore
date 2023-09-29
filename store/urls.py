from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:slug>/", views.product_detail_view, name="product_detail"),
    # htmx routes
    path(
        "<int:pk>/<str:color>/images/", views.product_images_view, name="product_images"
    ),
]
