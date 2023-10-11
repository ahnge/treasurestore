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


def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    slug = product.slug
    if request.method == "POST" and request.META.get("HTTP_HX_REQUEST"):
        size = request.POST.get("size")
        color = request.POST.get("color")
        quantity = request.POST.get("quantity")
        print(quantity)

        # make sure quantity is greater than 0
        if int(quantity) <= 0:
            return redirect("store:product_detail", slug)

        cart = request.session.get("cart", {})

        cart_item_name = f"{product_id}-{size}-{color}"

        if cart_item_name in cart:
            cart[cart_item_name]["quantity"] += int(quantity)
        else:
            cart_item = {
                "key": cart_item_name,
                "product_id": product_id,
                "name": product.name,
                "price": int(product.price),
                "size": size,
                "color": color,
                "quantity": int(quantity),
            }
            cart[cart_item_name] = cart_item

        request.session["cart"] = cart
        return render(request, "store/htmx/cart_count.html", {"cart_count": len(cart)})
    return redirect("store:product_detail", slug)


# def remove_from_cart(request, product_id):
#     cart = request.session.get("cart", {})

#     if product_id in cart:
#         if cart[product_id]["quantity"] > 1:
#             cart[product_id]["quantity"] -= 1
#         else:
#             del cart[product_id]

#     request.session["cart"] = cart
#     return redirect("cart:cart_view")


def view_cart(request):
    cart = request.session.get("cart", {})
    print(cart)
    return render(request, "store/cart.html", {"cart": cart})


def increment_cart_item(request, key):
    if request.method == "GET" and request.META.get("HTTP_HX_REQUEST"):
        # Update the session
        cart = request.session.get("cart", {})
        if cart.get(key):
            cart[key]["quantity"] += 1
            request.session["cart"] = cart

        return render(request, "store/htmx/cart_count.html", {"cart_count": len(cart)})
    return redirect("store:index")


def decrement_cart_item(request, key):
    if request.method == "GET" and request.META.get("HTTP_HX_REQUEST"):
        # Update the session
        cart = request.session.get("cart", {})
        if cart.get(key):
            if cart[key]["quantity"] == 1:
                cart.pop(key)
            else:
                cart[key]["quantity"] -= 1
            request.session["cart"] = cart

        return render(request, "store/htmx/cart_count.html", {"cart_count": len(cart)})

    return redirect("store:index")
