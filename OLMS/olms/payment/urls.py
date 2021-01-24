from django.urls import path,include
from . import views
from users import urls

urlpatterns = [
    path("checkout/<int:aptid>", views.checkout, name='checkout'),
    path("checkout/success/", views.success, name='success'),
    
]