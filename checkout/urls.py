from django.urls import path
from . import views

app_name = "checkout"

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success_view, name='success'),
    path('cancelled/', views.cancelled_view, name='cancelled'),
    path('create-checkout-session/', views.create_checkout_session),
    path('config/', views.stripe_config),
]
