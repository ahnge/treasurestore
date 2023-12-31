from django.contrib import admin
from .models import (
    Category,
    SubCategory,
    Color,
    Order,
    OrderItem,
    Product,
    ProductImage,
    ShippingAddress,
    Size,
    ProductColor,
    Graphic,
)
from sorl.thumbnail.admin import AdminImageMixin


class ProductColorInline(AdminImageMixin, admin.TabularInline):
    model = ProductColor
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "created_at"]
    list_filter = ["sub_category"]
    search_fields = ["name", "description"]
    inlines = [ProductColorInline]


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ShippingAddress)
admin.site.register(Graphic)
