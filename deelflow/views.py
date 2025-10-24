# ===============================
# STRIPE PAYMENT FUNCTIONS
# ===============================

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth.models import User
from .models import SubscriptionPackage, Subscription
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import stripe
import json
import logging

# Set up Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)

# Function 1: Get all available subscription packages (pricing plans)
@api_view(['GET'])
def get_subscription_packages(request):
    """Returns all available subscription plans"""
    try:
        packages = SubscriptionPackage.objects.all().order_by('amount')
        package_data = []
        
        for package in packages:
            package_data.append({
                'id': package.id,
                'name': package.name,
                'description': package.description,
                'amount': str(package.amount),
                'currency': package.currency,
                'interval': package.interval
            })
        
        return Response({
            'status': 'success',
            'packages': package_data
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=400)


# Function 2: Create a Stripe checkout session (payment page)
@api_view(['POST'])
def create_checkout_session(request):
    """Creates a Stripe checkout session for subscription"""
    try:
        package_id = request.data.get('package_id')
        if not package_id:
            return Response({
                'status': 'error',
                'message': 'package_id is required'
            }, status=400)

        # Get the subscription package
        package = SubscriptionPackage.objects.get(id=package_id)
        
        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='subscription',
            line_items=[{
                'price': package.stripe_price_id,
                'quantity': 1,
            }],
            success_url=f'{settings.FRONTEND_URL}/success?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{settings.FRONTEND_URL}/cancel',
            metadata={
                'package_id': package.id,
                'user_id': request.user.id if request.user.is_authenticated else None,
            }
        )
        
        return Response({
            'status': 'success',
            'checkout_url': checkout_session.url
        })
        
    except SubscriptionPackage.DoesNotExist:
        return Response({
            'status': 'error', 
            'message': 'Package not found'
        }, status=404)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=400)


# Function 3: Handle Stripe webhooks (when payment is completed)
@csrf_exempt
@api_view(['POST'])
def stripe_webhook(request):
    """Handle Stripe webhook events"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    # For local testing, skip signature verification
    if settings.DEBUG:
        try:
            event = json.loads(payload.decode('utf-8'))
            logger.info(f"✅ LOCAL WEBHOOK TEST - Event received: {event.get('type', 'unknown')}")
        except json.JSONDecodeError:
            return JsonResponse({'status': 'invalid payload'}, status=400)
    else:
        try:
            # Verify webhook signature (only in production)
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            return JsonResponse({'status': 'invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError:
            return JsonResponse({'status': 'invalid signature'}, status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Get package and user info from metadata
        package_id = session['metadata'].get('package_id')
        user_id = session['metadata'].get('user_id')
        
        if package_id and user_id:
            # Create subscription record
            package = SubscriptionPackage.objects.get(id=package_id)
            user = User.objects.get(id=user_id)
            
            Subscription.objects.create(
                user=user,
                package=package,
                stripe_subscription_id=session['subscription'],
                stripe_customer_id=session['customer'],
                status='active'
            )
    
    elif event['type'] == 'customer.subscription.deleted':
        subscription_data = event['data']['object']
        
        # Update subscription status to canceled
        try:
            subscription = Subscription.objects.get(
                stripe_subscription_id=subscription_data['id']
            )
            subscription.status = 'canceled'
            subscription.save()
        except Subscription.DoesNotExist:
            pass
    
    return JsonResponse({'status': 'success'})


# Function 4: Get current user's subscription
@api_view(['GET'])
def get_user_subscription(request):
    """Get current user's subscription details"""
    if not request.user.is_authenticated:
        return Response({
            'status': 'error',
            'message': 'User not authenticated'
        }, status=401)
    
    try:
        subscription = Subscription.objects.filter(
            user=request.user
        ).select_related('package').order_by('-created_at').first()
        
        if subscription:
            return Response({
                'status': 'success',
                'subscription': {
                    'id': subscription.id,
                    'package_name': subscription.package.name,
                    'status': subscription.status,
                    'amount': str(subscription.package.amount),
                    'interval': subscription.package.interval,
                    'created_at': subscription.created_at
                }
            })
        else:
            return Response({
                'status': 'success',
                'subscription': None
            })
            
    except Exception as e:
            return Response({
            'status': 'error',
            'message': str(e)
                }, status=400)


# Function 5: Get configuration for frontend
@api_view(['GET'])
def get_config(request):
    """Get configuration settings for frontend"""
    return Response({
        'status': 'success',
        'config': {
            'backend_url': settings.BACKEND_URL,
            'frontend_url': settings.FRONTEND_URL,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        }
    })