from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<str:slug>/", views.product_detail_view, name="product_detail"),
    # htmx routes
    path(
        "<int:pk>/<str:color>/images/", views.product_images_view, name="product_images"
    ),
    # cart
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "cart/increment/<str:key>/",
        views.increment_cart_item,
        name="increment_cart_item",
    ),
    path(
        "cart/decrement/<str:key>/",
        views.decrement_cart_item,
        name="decrement_cart_item",
    ),
    path("cart/view/", views.view_cart, name="cart_view"),
    # path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]
