from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    Product,
    ProductColor,
    Color,
    Graphic,
    OrderItem,
    Size,
    Order,
    Category,
    SubCategory,
)
from .forms import OrderForm, ShippingAddressForm


def index(request):
    products = Product.objects.all()[:5]
    graphics = Graphic.objects.all()
    cart = request.session.get("cart", {})
    context = {
        "products": products,
        "graphics": graphics,
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
    order_form = OrderForm()
    address_form = ShippingAddressForm()
    if request.method == "POST":
        address_form = ShippingAddressForm(request.POST)
        order_form = OrderForm(request.POST)
        if address_form.is_valid() and order_form.is_valid():
            # Ensure guests provide ph no and name
            if not request.user.is_authenticated:
                if not order_form.cleaned_data.get(
                    "guest_name"
                ) or not order_form.cleaned_data.get("guest_phone_number"):
                    print("guest error")
                    order_form.add_error("guest_name", "This field is required")
                    order_form.add_error("guest_phone_number", "This field is required")
                    return render(
                        request,
                        "store/make_order.html",
                        {
                            "order_form": order_form,
                            "address_form": address_form,
                            "cart_count": len(cart),
                        },
                    )
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
    cart = request.session.get("cart", [])
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        phone_number = phone_number.replace(" ", "")
        orders = Order.objects.filter(
            guest_phone_number__exact=phone_number, is_guest_order=True
        )
        # Injecting the order total value into each order record
        for order in orders:
            order_total = 0
            for order_item in order.order_items.all():
                order_total += order_item.quantity * order_item.product.price
            order.order_total = int(order_total)
            order.save()
        context = {"orders": orders, "cart_count": len(cart)}
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
        context = {"orders": orders, "cart_count": len(cart)}
        return render(request, "store/your_orders.html", context)
    else:
        return render(
            request, "store/phone_number_form.html", {"cart_count": len(cart)}
        )


def ordering_process(request):
    return render(request, "store/ordering_process.html")


def terms(request):
    return render(request, "store/terms.html")


def order_status(request):
    return render(request, "store/order_status.html")


def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all()

    if request.META.get("HTTP_HX_REQUEST"):
        colors = request.GET.getlist("color")
        min_price = request.GET.get("min")
        max_price = request.GET.get("max")
        sizes = request.GET.getlist("size")

        # Start with a base queryset
        filtered_products = products

        # Filter by colors
        if colors:
            filtered_products = filtered_products.filter(
                productcolor__color__name__in=colors
            )

        # Filter by minimum price
        if min_price:
            filtered_products = filtered_products.filter(price__gte=int(min_price))

        # Filter by maximum price
        if max_price:
            filtered_products = filtered_products.filter(price__lte=int(max_price))

        # Filter by size
        if sizes and len(sizes) > 0 and sizes[0] != "":
            filtered_products = filtered_products.filter(sizes__name__in=sizes)

        context = {
            "products": filtered_products,
        }

        return render(request, "store/partials/_products_grid.html", context)

    context = {
        "products": products,
        "categories": categories,
        "colors": colors,
        "sizes": sizes,
    }
    return render(request, "store/shop.html", context)


def specific_shop(request, category, sub_category):
    products = Product.objects.all()
    categories = Category.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all()

    # Start with a base queryset
    filtered_products = products

    # Filter products based on category and sub category
    category_instance = Category.objects.get(name=category)
    sub_category_instance = SubCategory.objects.get(
        name=sub_category, parent_category=category_instance
    )
    filtered_products = filtered_products.filter(sub_category=sub_category_instance)

    if request.META.get("HTTP_HX_REQUEST"):
        colors = request.GET.getlist("color")
        min_price = request.GET.get("min")
        max_price = request.GET.get("max")
        sizes = request.GET.getlist("size")

        # Filter by colors
        if colors:
            filtered_products = filtered_products.filter(
                productcolor__color__name__in=colors
            )

        # Filter by minimum price
        if min_price:
            filtered_products = filtered_products.filter(price__gte=int(min_price))

        # Filter by maximum price
        if max_price:
            filtered_products = filtered_products.filter(price__lte=int(max_price))

        # Filter by size
        if sizes and len(sizes) > 0 and sizes[0] != "":
            filtered_products = filtered_products.filter(sizes__name__in=sizes)

        context = {
            "products": filtered_products,
        }

        return render(request, "store/partials/_products_grid.html", context)

    context = {
        "products": filtered_products,
        "categories": categories,
        "colors": colors,
        "sizes": sizes,
        "category": category,
        "sub_category": sub_category,
    }
    return render(request, "store/shop.html", context)
