from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, NewsLetterSubscribersForm
from .models import NewsLetterSubcribers


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration success.")
            return redirect("store:index")
        return render(request, "registration/register.html", {"form": form})
    elif request.method == "GET":
        form = CustomUserCreationForm()
        return render(request, "registration/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logined.")
            return redirect("store:index")
        else:
            form = AuthenticationForm(request.POST)
            return render(
                request,
                "registration/login.html",
                {
                    "form": form,
                    "error": "Please enter a correct username and password.",
                },
            )
    elif request.method == "GET":
        form = AuthenticationForm()
        return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("store:index")


def newsletter_subscribe(request):
    if request.META.get("HTTP_HX_REQUEST") and request.method == "POST":
        form = NewsLetterSubscribersForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if not NewsLetterSubcribers.objects.filter(email=email).exists():
                form.save()
                return render(
                    request,
                    "accounts/htmx/newsletter-message.html",
                    {"alert": "success", "message": "Success"},
                )
            else:
                return render(
                    request,
                    "accounts/htmx/newsletter-message.html",
                    {"message": "Already subcribed!", "alert": "error"},
                )
        return render(
            request,
            "accounts/htmx/newsletter-message.html",
            {"message": "Error!", "alert": "error"},
        )

    return redirect("store:index")
