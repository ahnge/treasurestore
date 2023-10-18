from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import CustomUser, NewsLetterSubcribers


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=16, required=True, help_text="Required. Enter your phone number."
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    def clean_first_name(self):
        """Make first name to be required"""
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise ValidationError("This field is required.", code="no_first_name")
        return first_name

    def clean_last_name(self):
        """Make last name to be required"""
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise ValidationError("This field is required.", code="no_last_name")
        return last_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number:
            raise forms.ValidationError(
                "This field is required.", code="no_phone_number"
            )
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        custom_user = CustomUser(
            user=user, phone_number=self.cleaned_data["phone_number"]
        )
        if commit:
            custom_user.save()
        return user


class NewsLetterSubscribersForm(forms.ModelForm):
    class Meta:
        model = NewsLetterSubcribers
        fields = ["email"]
