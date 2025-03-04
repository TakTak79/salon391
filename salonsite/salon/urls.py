from django.urls import path

from salon import views
from django.conf.urls.static import static
from django.conf import settings


# from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name ="about"),
    path("booking/", views.booking, name="booking"),
    path("services/", views.services, name="services"),
    path("shop/", views.shop, name="shop"),
    # path("cart/", views.cart, name="cart"),
     path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('login/', views.login_page, name='login_page'),    # Login page
    path('register/', views.register_page, name='register'),  # Registration page
    path('logout/', views.logout_view, name="logout"),
    path('change_password/', views.change_password, name="change_password"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)