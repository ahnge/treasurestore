from django.shortcuts import render, get_object_or_404
from .models import Product, ProductColor


def index(request):
    products = Product.objects.all()[:5]
    context = {"products": products}
    return render(request, "store/index.html", context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_colors = ProductColor.objects.filter(product=product)
    print(product_colors)
    print(product_colors.first().images.all())
    context = {"product": product, "product_colors": product_colors}
    return render(request, "store/product_detail.html", context)
