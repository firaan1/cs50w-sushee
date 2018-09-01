from django.urls import path

from . import views

urlpatterns = [
    path("<str:dress_type>/<int:dress_id>", views.dressitem, name="dressitem"),
    path("additems", views.additems, name="additems"),
    path("collections", views.collections, name="collections"),
    path("histories", views.histories, name="histories"),
    path("cart", views.cart, name="cart"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("", views.index, name="index")
]
