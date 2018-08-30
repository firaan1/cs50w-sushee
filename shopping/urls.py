from django.urls import path

from . import views

urlpatterns = [
    path("additems", views.additems, name="additems"),
    path("order", views.order, name="order"),
    path("model_form_upload", views.model_form_upload, name="model_form_upload"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("", views.index, name="index")
]
