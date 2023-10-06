from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductColor, Color, Graphic


def index(request):
    products = Product.objects.all()[:5]
    featured_main = Graphic.objects.get(name="featured main")
    featured_women = Graphic.objects.get(name="featured women")
    featured_men = Graphic.objects.get(name="featured men")
    featured_kid = Graphic.objects.get(name="featured kid")
    context = {
        "products": products,
        "featured_main": featured_main,
        "featured_women": featured_women,
        "featured_men": featured_men,
        "featured_kid": featured_kid,
    }
    return render(request, "store/index.html", context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_colors = ProductColor.objects.filter(product=product)
    context = {"product": product, "product_colors": product_colors}
    return render(request, "store/product_detail.html", context)


def product_images_view(request, pk, color):
    if request.META.get("HTTP_HX_REQUEST"):
        product = get_object_or_404(Product, pk=pk)
        c = get_object_or_404(Color, name=color)
        product_color = ProductColor.objects.get(product=product, color=c)
        context = {"product": product, "product_color": product_color}
        return render(request, "store/htmx/product_images.html", context)
    return redirect("store:index")
