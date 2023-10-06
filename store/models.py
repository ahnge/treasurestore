from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from sorl.thumbnail import ImageField


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = ImageField(upload_to="product_images/")
    alt_text = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.image.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sizes = models.ManyToManyField("Size", blank=True)
    categories = models.ManyToManyField(Category)
    main_image = models.ForeignKey(
        ProductImage, on_delete=models.CASCADE, blank=True, null=True
    )
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate a slug from the product name
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super(Product, self).save(*args, **kwargs)


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey("Color", on_delete=models.CASCADE)
    images = models.ManyToManyField(
        ProductImage, related_name="product_colors", blank=True
    )

    def __str__(self):
        return f"{self.product} - {self.color}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    guest_name = models.CharField(max_length=100, null=True, blank=True)
    guest_phone_number = models.TextField(null=True, blank=True)
    is_guest_order = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    confirm = models.BooleanField(default=False)

    def __str__(self):
        return f"Order Item #{self.pk} - {self.product.name}"


class ShippingAddress(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="shipping_address"
    )
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)

    def __str__(self):
        return f"Shipping Address for Order #{self.order.pk}"


class Graphic(models.Model):
    name = models.TextField(max_length=64)
    image = ImageField(upload_to="graphics")
    alt_text = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return self.name
