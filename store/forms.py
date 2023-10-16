from django import forms
from .models import Order, ShippingAddress


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["guest_name", "guest_phone_number", "accepted_terms"]

    def clean_guest_phone_number(self):
        guest_phone_number = self.cleaned_data.get("guest_phone_number", "")
        guest_phone_number = guest_phone_number.replace(" ", "")
        return guest_phone_number

    def clean_accepted_terms(self):
        accepted_terms = self.cleaned_data.get("accepted_terms")
        if not accepted_terms:
            raise forms.ValidationError(
                "You must accept the terms and conditions to place an order."
            )
        return accepted_terms

    def save(self, commit=True):
        # Clean the guest_phone_number field before saving
        self.cleaned_data["guest_phone_number"] = self.clean_guest_phone_number()
        return super(OrderForm, self).save(commit)


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ["address", "city", "state"]
