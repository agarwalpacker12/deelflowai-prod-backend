from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Stripe Payment URLs (keep these as they're payment-specific)
    path('api/subscription-packages/', views.get_subscription_packages, name='subscription-packages'),
    path('api/create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('api/stripe-webhook/', views.stripe_webhook, name='stripe-webhook'),
    path('api/user-subscription/', views.get_user_subscription, name='user-subscription'),
    path('api/config/', views.get_config, name='config'),
]