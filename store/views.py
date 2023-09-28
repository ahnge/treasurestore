from django.shortcuts import render
from .models import Product


def index(request):
    products = Product.objects.all()[:5]
    context = {"products": products}
    return render(request, "store/index.html", context)
