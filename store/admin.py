from django.contrib import admin
from .models import (
    Category,
    Color,
    Order,
    OrderItem,
    Product,
    ProductColorSize,
    ProductImage,
    ShippingAddress,
    Size,
)


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]
    list_filter = ["categories"]
    search_fields = ["title", "description"]


admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductColorSize)
admin.site.register(ProductImage)
admin.site.register(ShippingAddress)
admin.site.register(Size)
