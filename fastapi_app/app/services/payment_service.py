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

# Configure Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_your_stripe_secret_key_here')

logger = logging.getLogger(__name__)

class PaymentService:
    """Service for handling all payment operations with Stripe"""
    
    def __init__(self):
        self.stripe = stripe
        self.webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_your_webhook_secret_here')
    
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
            session_data = {
                'payment_method_types': ['card'],
                'line_items': [{
                    'price': price_id,
                    'quantity': 1,
                }],
                'mode': 'subscription',
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
