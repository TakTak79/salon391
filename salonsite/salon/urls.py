from django.urls import path

from salon import views

# from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name ="about"),
    path("booking/", views.booking, name="booking"),
    path("services/", views.services, name="services"),
    path("shop/", views.shop, name="shop"),
    path("cart/", views.cart, name="cart"),
    path('login/', views.login_page, name='login_page'),    # Login page
    path('register/', views.register_page, name='register'),  # Registration page
    path('logout/', views.logout_view, name="logout"),
    path('change_password/', views.change_password, name="change_password"),
]