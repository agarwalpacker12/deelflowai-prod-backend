"""
Payment Service - Stripe Integration and Payment Processing
Handles all payment-related operations for the SaaS platform
"""

import stripe
import os
from typing import Dict, List, Optional, Any
from decimal import Decimal
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent.parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path, override=True)  # Force override to ensure latest values
    print(f"🔑 PaymentService: Loading .env from {env_path}")

# Configure Stripe - load directly from .env
stripe_secret_key = os.getenv('STRIPE_SECRET_KEY', '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')
if stripe_secret_key and stripe_secret_key != 'sk_test_your_key_here':
    stripe.api_key = stripe_secret_key
    print(f"🔑 PaymentService: Stripe API key set at module level: {stripe_secret_key[:20]}...")
else:
    print(f"⚠️  PaymentService: Stripe API key not found or invalid: {stripe_secret_key[:30] if stripe_secret_key else 'None'}...")


logger = logging.getLogger(__name__)

class PaymentService:
    """Service for handling all payment operations with Stripe"""
    
    def __init__(self):
        self.stripe = stripe
        self.webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_your_webhook_secret_here')
        
        # Set Stripe API key dynamically from environment (double-check)
        api_key = os.getenv('STRIPE_SECRET_KEY', '')
        if api_key and api_key != 'sk_test_your_key_here':
            stripe.api_key = api_key
            print(f"🔑 PaymentService: Stripe API key configured in __init__: {api_key[:20]}...")
        else:
            print(f"⚠️  PaymentService: Invalid or missing Stripe API key in __init__: {api_key[:30] if api_key else 'None'}...")
            # Try loading from .env again
            env_path = Path(__file__).parent.parent.parent.parent / ".env"
            if env_path.exists():
                load_dotenv(env_path, override=True)
                api_key = os.getenv('STRIPE_SECRET_KEY', '')
                if api_key and api_key != 'sk_test_your_key_here':
                    stripe.api_key = api_key
                    print(f"🔑 PaymentService: Stripe API key reloaded: {api_key[:20]}...")
    
    async def create_payment_intent(self, amount: Decimal, currency: str = "usd", 
                                  metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a Stripe payment intent"""
        try:
            # Convert Decimal to cents for Stripe
            amount_cents = int(amount * 100)
            
            intent = self.stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=currency,
                metadata=metadata or {},
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            
            return {
                "status": "success",
                "data": {
                    "id": intent.id,
                    "client_secret": intent.client_secret,
                    "amount": amount,
                    "currency": currency,
                    "status": intent.status
                }
            }
        except Exception as e:
            logger.error(f"Error creating payment intent: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to create payment intent: {str(e)}"
            }
    
    async def create_checkout_session(self, price_id: str, customer_id: Optional[str] = None,
                                    success_url: str = None, cancel_url: str = None) -> Dict[str, Any]:
        """Create a Stripe checkout session for subscriptions"""
        try:
            price = self.stripe.Price.retrieve(price_id)
            mode = 'subscription' if price.recurring else 'payment'
            print("mode:", mode)
            session_data = {
                'payment_method_types': ['card'],
                'line_items': [{
                    'price': price_id,
                    'quantity': 1,
                }],
                'mode': mode,
                'success_url': success_url or 'http://localhost:5173/payment/success?session_id={CHECKOUT_SESSION_ID}',
                'cancel_url': cancel_url or 'http://localhost:5173/payment/cancel',
            }
            
            if customer_id:
                session_data['customer'] = customer_id
            
            session = self.stripe.checkout.Session.create(**session_data)
            
            return {
                "status": "success",
                "data": {
                    "session_id": session.id,
                    "url": session.url,
                    "customer_id": session.customer
                }
            }
        except Exception as e:
            logger.error(f"Error creating checkout session: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to create checkout session: {str(e)}"
            }
    
    async def create_customer_portal_session(self, customer_id: str, return_url: str = None) -> Dict[str, Any]:
        """Create a customer portal session for subscription management"""
        try:
            session = self.stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url or 'http://localhost:5173/dashboard'
            )
            
            return {
                "status": "success",
                "data": {
                    "url": session.url
                }
            }
        except Exception as e:
            logger.error(f"Error creating customer portal session: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to create customer portal session: {str(e)}"
            }
    
    async def get_subscription_packages(self) -> Dict[str, Any]:
        """Get available subscription packages"""
        try:
            # Find .env file - try multiple possible locations
            possible_paths = [
                Path(__file__).parent.parent.parent.parent / ".env",  # From payment_service.py: ../../../../.env
                Path(__file__).parent.parent.parent.parent.parent / ".env",  # One level up (if in subdirectory)
                Path.cwd() / ".env",  # Current working directory
                Path.cwd().parent / ".env",  # Parent of current directory
            ]
            
            env_path = None
            for path in possible_paths:
                absolute_path = path.resolve()
                print(f"🔍 Checking for .env at: {absolute_path}")
                if absolute_path.exists():
                    env_path = absolute_path
                    print(f"✅ Found .env file at: {absolute_path}")
                    break
            
            if env_path and env_path.exists():
                print(f"🔑 Loading .env from: {env_path}")
                load_dotenv(env_path, override=True)
            
            # Get key directly from .env, not from os.environ (which might have defaults)
            stripe_key = os.getenv("STRIPE_SECRET_KEY", "")
            
            # If key is still placeholder or empty, try reading .env directly
            if (not stripe_key or stripe_key == 'sk_test_your_key_here' or 'test' in stripe_key.lower()) and env_path:
                # Read .env file directly
                try:
                    if env_path.exists():
                        with open(env_path, 'r') as f:
                            for line in f:
                                if line.startswith('STRIPE_SECRET_KEY='):
                                    stripe_key = line.split('=', 1)[1].strip()
                                    break
                except Exception as e:
                    print(f"⚠️  Error reading .env file in first attempt: {e}")
                    pass
            
            # CRITICAL: Ensure we have a valid Stripe key before making API calls
            if not stripe_key or not stripe_key.startswith('sk_live_'):
                # Final fallback - read .env file directly line by line
                print(f"⚠️  Key not found via env var, reading .env directly from: {env_path if env_path else 'NOT FOUND'}...")
                if env_path and env_path.exists():
                    try:
                        with open(env_path, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                            print(f"📄 Reading .env file ({len(lines)} lines)...")
                            for line_num, line in enumerate(lines, 1):
                                line = line.strip()
                                # Skip comments and empty lines
                                if not line or line.startswith('#'):
                                    continue
                                if line.startswith('STRIPE_SECRET_KEY='):
                                    raw_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                                    print(f"🔑 Found STRIPE_SECRET_KEY on line {line_num}: {raw_key[:30]}...")
                                    if raw_key.startswith('sk_live_'):
                                        stripe_key = raw_key
                                        print(f"✅ Valid live key found in .env: {stripe_key[:30]}...")
                                        break
                                    else:
                                        print(f"⚠️  Key on line {line_num} doesn't start with 'sk_live_': {raw_key[:7]}...")
                    except Exception as e:
                        print(f"❌ Error reading .env file: {e}")
                        import traceback
                        traceback.print_exc()
                else:
                    print(f"❌ .env file not found at any expected location!")
            
            # Set the key if we found a valid one
            if stripe_key and stripe_key.startswith('sk_live_'):
                stripe.api_key = stripe_key
                self.stripe.api_key = stripe_key  # Also set on instance
                print(f"🔑 Stripe API key SET: {stripe_key[:30]}...")
                print(f"🔑 Key length: {len(stripe_key)} characters")
                print(f"🔑 Key preview: {stripe_key[:50]}...{stripe_key[-10:]}")
            else:
                print(f"❌ CRITICAL: No valid Stripe key found!")
                print(f"   Checked env_path: {env_path}")
                print(f"   File exists: {env_path.exists() if env_path else 'N/A (path is None)'}")
                print(f"   stripe_key value: {stripe_key[:50] if stripe_key else 'None'}...")
                print(f"   Current stripe.api_key: {stripe.api_key[:30] if stripe.api_key else 'NOT SET'}...")
                raise ValueError("Stripe API key not configured. Please set STRIPE_SECRET_KEY in .env file.")
            
            # Verify key is set before API call
            if not stripe.api_key or not stripe.api_key.startswith('sk_live_'):
                raise ValueError(f"Stripe API key not properly set. Current value: {stripe.api_key[:30] if stripe.api_key else 'None'}")

            # Get products and prices from Stripe
            products = self.stripe.Product.list(active=True, limit=10)
            prices = self.stripe.Price.list(active=True, limit=50)
            
            packages = []
            for product in products.data:
                product_prices = [p for p in prices.data if p.product == product.id]
                if product_prices:
                    # Get the first price (you might want to handle multiple prices differently)
                    price = product_prices[0]
                    packages.append({
                        "id": product.id,
                        "name": product.name,
                        "description": product.description,
                        "price_id": price.id,
                        "amount": price.unit_amount / 100,  # Convert from cents
                        "currency": price.currency,
                        "interval": price.recurring.interval if price.recurring else None,
                        "features": product.metadata.get('features', '').split(',') if product.metadata.get('features') else []
                    })
            
            return {
                "status": "success",
                "data": {
                    "packages": packages,
                    "total": len(packages)
                }
            }
        except Exception as e:
            logger.error(f"Error getting subscription packages: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get subscription packages: {str(e)}"
            }
    
    async def get_customer_subscription(self, customer_id: str) -> Dict[str, Any]:
        """Get customer's current subscription"""
        try:
            subscriptions = self.stripe.Subscription.list(
                customer=customer_id,
                status='active',
                limit=1
            )
            
            if subscriptions.data:
                subscription = subscriptions.data[0]
                return {
                    "status": "success",
                    "data": {
                        "id": subscription.id,
                        "status": subscription.status,
                        "current_period_start": datetime.fromtimestamp(subscription.current_period_start),
                        "current_period_end": datetime.fromtimestamp(subscription.current_period_end),
                        "cancel_at_period_end": subscription.cancel_at_period_end,
                        "plan": {
                            "id": subscription.items.data[0].price.id,
                            "name": subscription.items.data[0].price.product.name,
                            "amount": subscription.items.data[0].price.unit_amount / 100
                        }
                    }
                }
            else:
                return {
                    "status": "success",
                    "data": None
                }
        except Exception as e:
            logger.error(f"Error getting customer subscription: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get customer subscription: {str(e)}"
            }
    
    async def get_customer_invoices(self, customer_id: str, limit: int = 10) -> Dict[str, Any]:
        """Get customer's invoice history"""
        try:
            invoices = self.stripe.Invoice.list(
                customer=customer_id,
                limit=limit
            )
            
            invoice_list = []
            for invoice in invoices.data:
                invoice_list.append({
                    "id": invoice.id,
                    "amount_paid": invoice.amount_paid / 100,
                    "currency": invoice.currency,
                    "status": invoice.status,
                    "created": datetime.fromtimestamp(invoice.created),
                    "invoice_pdf": invoice.invoice_pdf,
                    "hosted_invoice_url": invoice.hosted_invoice_url
                })
            
            return {
                "status": "success",
                "data": {
                    "invoices": invoice_list,
                    "total": len(invoice_list)
                }
            }
        except Exception as e:
            logger.error(f"Error getting customer invoices: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get customer invoices: {str(e)}"
            }
    
    async def get_revenue_metrics(self) -> Dict[str, Any]:
        """Get revenue and billing metrics"""
        try:
            # Get total revenue from all successful payments
            charges = self.stripe.Charge.list(limit=100)
            total_revenue = sum(charge.amount for charge in charges.data if charge.status == 'succeeded')
            
            # Get monthly recurring revenue
            subscriptions = self.stripe.Subscription.list(status='active', limit=100)
            mrr = sum(sub.items.data[0].price.unit_amount for sub in subscriptions.data) / 100
            
            # Get customer count
            customers = self.stripe.Customer.list(limit=100)
            customer_count = len(customers.data)
            
            return {
                "status": "success",
                "data": {
                    "total_revenue": total_revenue / 100,
                    "monthly_recurring_revenue": mrr,
                    "customer_count": customer_count,
                    "currency": "usd"
                }
            }
        except Exception as e:
            logger.error(f"Error getting revenue metrics: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get revenue metrics: {str(e)}"
            }
    
    async def verify_payment(self, session_id: str) -> Dict[str, Any]:
        """Verify payment completion"""
        try:
            session = self.stripe.checkout.Session.retrieve(session_id)
            
            if session.payment_status == 'paid':
                return {
                    "status": "success",
                    "data": {
                        "payment_status": "success",
                        "session_id": session_id,
                        "customer_id": session.customer,
                        "subscription_id": session.subscription
                    }
                }
            else:
                return {
                    "status": "error",
                    "message": "Payment not completed"
                }
        except Exception as e:
            logger.error(f"Error verifying payment: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to verify payment: {str(e)}"
            }
