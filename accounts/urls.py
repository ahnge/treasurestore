from django.urls import path

from .views import login_view, logout_view, register_view, newsletter_subscribe

app_name = "accounts"
urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("subsribe-newsletter/", newsletter_subscribe, name="subcribe_newsletter"),
]
