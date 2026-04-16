from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart),
    #path('remove/<int:item_id>/', views.remove_from_cart),
    path('remove/<int:product_id>/', views.remove_from_cart),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('checkout/', views.checkout, name='checkout'),
    path('logout/', views.user_logout, name='logout'),

]


