from django import forms
from .models import Order, ShippingAddress


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["guest_name", "guest_phone_number"]


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ["address", "city", "state"]
