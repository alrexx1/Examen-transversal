from django.urls import path
from .views import home, signup, profile, checkout, cart, products, buy, delete, sell

urlpatterns = [
    path('', home, name='home'),
    path('accounts/signup', signup, name='signup'),
    path('accounts/profile', profile, name='profile'),
    path('shopping/checkout', checkout, name='checkout'),
    path('shopping/products/<id>', products, name='products'),
    path('shopping/buy', buy, name='buy'),
    path('shopping/delete/<id>', delete, name='delete'),
    path('shopping/cart', cart, name='cart'),
    path('shopping/sell/<discount>', sell, name='sell')
]
