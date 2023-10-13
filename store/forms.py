from django import forms
from .models import Order, ShippingAddress


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["guest_name", "guest_phone_number"]

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        self.fields["guest_name"].required = True
        self.fields["guest_phone_number"].required = True

    def clean_guest_phone_number(self):
        guest_phone_number = self.cleaned_data.get("guest_phone_number", "")
        guest_phone_number = guest_phone_number.replace(" ", "")
        return guest_phone_number

    def save(self, commit=True):
        # Clean the guest_phone_number field before saving
        self.cleaned_data["guest_phone_number"] = self.clean_guest_phone_number()
        return super(OrderForm, self).save(commit)


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ["address", "city", "state"]
