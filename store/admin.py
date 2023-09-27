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
    ProductColor,
)


class ColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "created_at"]
    list_filter = ["categories"]
    search_fields = ["name", "description"]
    inlines = [ColorInline]


admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ShippingAddress)
