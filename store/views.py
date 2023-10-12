from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductColor, Color, Graphic, OrderItem, Size, Order
from .forms import OrderForm, ShippingAddressForm


def index(request):
    products = Product.objects.all()[:5]
    featured_main = Graphic.objects.get(name="featured main")
    featured_women = Graphic.objects.get(name="featured women")
    featured_men = Graphic.objects.get(name="featured men")
    featured_kid = Graphic.objects.get(name="featured kid")
    cart = request.session.get("cart", {})
    context = {
        "products": products,
        "featured_main": featured_main,
        "featured_women": featured_women,
        "featured_men": featured_men,
        "featured_kid": featured_kid,
        "cart_count": len(cart),
    }
    return render(request, "store/index.html", context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_colors = ProductColor.objects.filter(product=product)
    cart = request.session.get("cart", {})
    context = {
        "product": product,
        "product_colors": product_colors,
        "cart_count": len(cart),
    }
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

        # make sure quantity is greater than 0
        if int(quantity) <= 0:
            return redirect("store:product_detail", slug)

        cart = request.session.get("cart", {})

        cart_item_name = f"{product_id}-{size}-{color}"

        if cart_item_name in cart:
            cart[cart_item_name]["quantity"] += int(quantity)
            cart[cart_item_name]["total"] += int(product.price)
        else:
            cart_item = {
                "product_id": product_id,
                "name": product.name,
                "slug": slug,
                "price": int(product.price),
                "size": size,
                "color": color,
                "quantity": int(quantity),
                "total": int(product.price) * int(quantity),
            }
            cart[cart_item_name] = cart_item

        request.session["cart"] = cart
        return render(request, "store/htmx/cart_count.html", {"cart_count": len(cart)})
    return redirect("store:product_detail", slug)


def view_cart(request):
    cart = request.session.get("cart", {})
    return render(request, "store/cart.html", {"cart": cart, "cart_count": len(cart)})


def increment_cart_item(request, key):
    if request.method == "GET" and request.META.get("HTTP_HX_REQUEST"):
        # Update the session
        cart = request.session.get("cart", {})
        if cart.get(key):
            cart[key]["quantity"] += 1
            cart[key]["total"] += cart[key]["price"]
            request.session["cart"] = cart

        context = {
            "cart_count": len(cart),
            "cart_item_quantity": cart[key]["quantity"],
            "key": key,
        }
        return render(
            request,
            "store/htmx/cart_item_quantity_and_total.html",
            context,
        )
    return redirect("store:index")


def decrement_cart_item(request, key):
    if request.method == "GET" and request.META.get("HTTP_HX_REQUEST"):
        # Update the session
        cart = request.session.get("cart", {})
        cart_item_quantity = 0
        if cart.get(key):
            if cart[key]["quantity"] == 1:
                cart.pop(key)
            else:
                cart[key]["quantity"] -= 1
                cart[key]["total"] -= cart[key]["price"]
                cart_item_quantity = cart[key]["quantity"]
            request.session["cart"] = cart

        context = {
            "cart_count": len(cart),
            "cart_item_quantity": cart_item_quantity,
            "key": key,
        }
        return render(
            request,
            "store/htmx/cart_item_quantity_and_total.html",
            context,
        )

    return redirect("store:index")


def make_order(request):
    cart = request.session.get("cart", {})
    if request.method == "POST":
        address_form = ShippingAddressForm(request.POST)
        order_form = OrderForm(request.POST)
        if address_form.is_valid() and order_form.is_valid():
            # Save the order and address forms
            order = order_form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            else:
                order.is_guest_order = True
            order.save()

            address = address_form.save(commit=False)
            address.order = order
            address.save()

            # Create order items form cart session
            for _, cart_item in cart.items():
                product = get_object_or_404(Product, pk=cart_item["product_id"])
                color = get_object_or_404(Color, name=cart_item["color"])
                size = get_object_or_404(Size, name=cart_item["size"])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=cart_item["quantity"],
                    color=color,
                    size=size,
                )
            # Empty the cart session
            request.session["cart"] = {}
            return render(request, "store/order_finish.html")
    else:
        # Ensure items are in cart session
        if not cart:
            return redirect("store:cart_view")
        order_form = OrderForm()
        address_form = ShippingAddressForm()

    return render(
        request,
        "store/make_order.html",
        {
            "order_form": order_form,
            "address_form": address_form,
            "cart_count": len(cart),
        },
    )


def your_orders(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        orders = Order.objects.filter(guest_phone_number=phone_number)
        # Injecting the order total value into each order record
        for order in orders:
            order_total = 0
            for order_item in order.order_items.all():
                order_total += order_item.quantity * order_item.product.price
            order.order_total = int(order_total)
            order.save()
        context = {"orders": orders}
        return render(request, "store/your_orders.html", context)
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        # Injecting the order total value into each order record
        for order in orders:
            order_total = 0
            for order_item in order.order_items.all():
                order_total += order_item.quantity * order_item.product.price
            order.order_total = int(order_total)
            order.save()
        context = {"orders": orders}
        return render(request, "store/your_orders.html", context)
    else:
        return render(request, "store/phone_number_form.html")
