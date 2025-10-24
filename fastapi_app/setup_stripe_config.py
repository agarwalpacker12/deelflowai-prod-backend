#!/usr/bin/env python3
"""
Stripe Configuration Setup Script
Sets up Stripe products and prices for the SaaS platform
"""

import stripe
import os
from typing import Dict, List, Any

# Configure Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_your_stripe_secret_key_here')

class StripeSetup:
    """Setup Stripe products and prices for the SaaS platform"""
    
    def __init__(self):
        self.stripe = stripe
        self.products_created = []
        self.prices_created = []
    
    def create_saas_products(self) -> Dict[str, Any]:
        """Create SaaS subscription products"""
        print("Creating SaaS subscription products...")
        
        # Define SaaS plans
        plans = [
            {
                "name": "Starter Plan",
                "description": "Perfect for individual real estate agents getting started",
                "amount": 29.99,
                "interval": "month",
                "features": [
                    "Up to 10 properties",
                    "Basic AI analysis",
                    "Email campaigns",
                    "Standard support"
                ],
                "metadata": {
                    "max_properties": "10",
                    "ai_features": "basic",
                    "support_level": "standard"
                }
            },
            {
                "name": "Professional Plan",
                "description": "Ideal for growing real estate teams and agencies",
                "amount": 79.99,
                "interval": "month",
                "features": [
                    "Up to 100 properties",
                    "Advanced AI analysis",
                    "Multi-channel campaigns",
                    "Priority support",
                    "Team collaboration"
                ],
                "metadata": {
                    "max_properties": "100",
                    "ai_features": "advanced",
                    "support_level": "priority"
                }
            },
            {
                "name": "Enterprise Plan",
                "description": "Complete solution for large real estate organizations",
                "amount": 199.99,
                "interval": "month",
                "features": [
                    "Unlimited properties",
                    "Full AI suite",
                    "Custom integrations",
                    "24/7 support",
                    "White-label options",
                    "Advanced analytics"
                ],
                "metadata": {
                    "max_properties": "unlimited",
                    "ai_features": "full",
                    "support_level": "24/7"
                }
            },
            {
                "name": "Annual Starter",
                "description": "Starter plan with 2 months free (annual billing)",
                "amount": 299.99,
                "interval": "year",
                "features": [
                    "Up to 10 properties",
                    "Basic AI analysis",
                    "Email campaigns",
                    "Standard support",
                    "2 months free"
                ],
                "metadata": {
                    "max_properties": "10",
                    "ai_features": "basic",
                    "support_level": "standard",
                    "billing": "annual"
                }
            }
        ]
        
        results = []
        
        for plan in plans:
            try:
                # Create product
                product = self.stripe.Product.create(
                    name=plan["name"],
                    description=plan["description"],
                    metadata=plan["metadata"]
                )
                self.products_created.append(product)
                
                # Create price
                price = self.stripe.Price.create(
                    product=product.id,
                    unit_amount=int(plan["amount"] * 100),  # Convert to cents
                    currency="usd",
                    recurring={"interval": plan["interval"]},
                    metadata=plan["metadata"]
                )
                self.prices_created.append(price)
                
                result = {
                    "product_id": product.id,
                    "price_id": price.id,
                    "name": plan["name"],
                    "amount": plan["amount"],
                    "interval": plan["interval"],
                    "features": plan["features"]
                }
                results.append(result)
                
                print(f"✅ Created: {plan['name']} - ${plan['amount']}/{plan['interval']}")
                
            except Exception as e:
                print(f"❌ Failed to create {plan['name']}: {str(e)}")
                results.append({
                    "error": str(e),
                    "name": plan["name"]
                })
        
        return {
            "status": "success",
            "products_created": len(self.products_created),
            "prices_created": len(self.prices_created),
            "plans": results
        }
    
    def create_one_time_products(self) -> Dict[str, Any]:
        """Create one-time payment products"""
        print("\nCreating one-time payment products...")
        
        one_time_products = [
            {
                "name": "Property Analysis Report",
                "description": "Detailed AI-powered property analysis report",
                "amount": 49.99,
                "metadata": {
                    "type": "analysis",
                    "delivery": "instant"
                }
            },
            {
                "name": "Market Research Package",
                "description": "Comprehensive market research and insights",
                "amount": 99.99,
                "metadata": {
                    "type": "research",
                    "delivery": "24h"
                }
            },
            {
                "name": "Custom Integration",
                "description": "Custom API integration setup",
                "amount": 499.99,
                "metadata": {
                    "type": "integration",
                    "delivery": "7d"
                }
            }
        ]
        
        results = []
        
        for product_data in one_time_products:
            try:
                # Create product
                product = self.stripe.Product.create(
                    name=product_data["name"],
                    description=product_data["description"],
                    metadata=product_data["metadata"]
                )
                self.products_created.append(product)
                
                # Create price
                price = self.stripe.Price.create(
                    product=product.id,
                    unit_amount=int(product_data["amount"] * 100),
                    currency="usd",
                    metadata=product_data["metadata"]
                )
                self.prices_created.append(price)
                
                result = {
                    "product_id": product.id,
                    "price_id": price.id,
                    "name": product_data["name"],
                    "amount": product_data["amount"],
                    "type": "one_time"
                }
                results.append(result)
                
                print(f"✅ Created: {product_data['name']} - ${product_data['amount']}")
                
            except Exception as e:
                print(f"❌ Failed to create {product_data['name']}: {str(e)}")
                results.append({
                    "error": str(e),
                    "name": product_data["name"]
                })
        
        return {
            "status": "success",
            "products_created": len([r for r in results if "error" not in r]),
            "products": results
        }
    
    def setup_webhook_endpoints(self) -> Dict[str, Any]:
        """Setup Stripe webhook endpoints"""
        print("\nSetting up webhook endpoints...")
        
        webhook_urls = [
            "https://your-domain.com/webhooks/stripe",
            "http://localhost:8140/webhooks/stripe"  # For development
        ]
        
        webhook_events = [
            "payment_intent.succeeded",
            "payment_intent.payment_failed",
            "checkout.session.completed",
            "customer.subscription.created",
            "customer.subscription.updated",
            "customer.subscription.deleted",
            "invoice.payment_succeeded",
            "invoice.payment_failed"
        ]
        
        results = []
        
        for url in webhook_urls:
            try:
                endpoint = self.stripe.WebhookEndpoint.create(
                    url=url,
                    enabled_events=webhook_events
                )
                
                result = {
                    "id": endpoint.id,
                    "url": endpoint.url,
                    "status": endpoint.status,
                    "events": len(endpoint.enabled_events)
                }
                results.append(result)
                
                print(f"✅ Created webhook: {url}")
                
            except Exception as e:
                print(f"❌ Failed to create webhook {url}: {str(e)}")
                results.append({
                    "error": str(e),
                    "url": url
                })
        
        return {
            "status": "success",
            "webhooks_created": len([r for r in results if "error" not in r]),
            "webhooks": results
        }
    
    def generate_config_file(self) -> str:
        """Generate configuration file with all created IDs"""
        config = {
            "stripe": {
                "secret_key": "sk_test_your_stripe_secret_key_here",
                "publishable_key": "pk_test_your_stripe_publishable_key_here",
                "webhook_secret": "whsec_your_webhook_secret_here"
            },
            "products": {
                "subscription_plans": [
                    {
                        "name": plan["name"],
                        "product_id": plan["product_id"],
                        "price_id": plan["price_id"],
                        "amount": plan["amount"],
                        "interval": plan["interval"]
                    }
                    for plan in self.products_created
                    if hasattr(plan, 'metadata') and 'max_properties' in plan.metadata
                ],
                "one_time_products": [
                    {
                        "name": plan["name"],
                        "product_id": plan["product_id"],
                        "price_id": plan["price_id"],
                        "amount": plan["amount"]
                    }
                    for plan in self.products_created
                    if hasattr(plan, 'metadata') and 'type' in plan.metadata
                ]
            }
        }
        
        config_file = "stripe_config.json"
        with open(config_file, 'w') as f:
            import json
            json.dump(config, f, indent=2)
        
        return config_file
    
    def run_setup(self) -> Dict[str, Any]:
        """Run complete Stripe setup"""
        print("🚀 Starting Stripe Configuration Setup")
        print("=" * 60)
        
        # Create subscription products
        subscription_result = self.create_saas_products()
        
        # Create one-time products
        one_time_result = self.create_one_time_products()
        
        # Setup webhooks
        webhook_result = self.setup_webhook_endpoints()
        
        # Generate config file
        config_file = self.generate_config_file()
        
        print(f"\n📄 Configuration saved to: {config_file}")
        
        return {
            "status": "success",
            "subscription_products": subscription_result,
            "one_time_products": one_time_result,
            "webhooks": webhook_result,
            "config_file": config_file,
            "summary": {
                "total_products": len(self.products_created),
                "total_prices": len(self.prices_created),
                "subscription_plans": len([p for p in self.products_created if hasattr(p, 'metadata') and 'max_properties' in p.metadata]),
                "one_time_products": len([p for p in self.products_created if hasattr(p, 'metadata') and 'type' in p.metadata])
            }
        }

if __name__ == "__main__":
    setup = StripeSetup()
    result = setup.run_setup()
    
    print("\n🎉 Stripe Setup Complete!")
    print("=" * 60)
    print(f"Products Created: {result['summary']['total_products']}")
    print(f"Prices Created: {result['summary']['total_prices']}")
    print(f"Subscription Plans: {result['summary']['subscription_plans']}")
    print(f"One-time Products: {result['summary']['one_time_products']}")
    print(f"\nConfiguration file: {result['config_file']}")
    print("\nNext steps:")
    print("1. Update your .env file with the Stripe keys")
    print("2. Configure webhook endpoints in Stripe dashboard")
    print("3. Test the payment system with the test script")
