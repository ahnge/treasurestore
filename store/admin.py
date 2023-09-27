from django.contrib import admin
from .models import (
    Category,
    Color,
    Order,
    OrderItem,
    Product,
    ProductImage,
    ShippingAddress,
    Size,
)


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "created_at"]
    list_filter = ["categories"]
    search_fields = ["name", "description"]


admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ShippingAddress)
