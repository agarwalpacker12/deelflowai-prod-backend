

from django.db import models

# --- Campaign Models for Multi-Channel Outreach ---

# --- Outreach Campaign Model ---
class OutreachCampaign(models.Model):
    CHANNEL_CHOICES = [
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('voice', 'Voice'),
        ('social', 'Social Media'),
        ('mail', 'Direct Mail'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    message_template = models.TextField()
    scheduled_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.channel})"

class CampaignRecipient(models.Model):
    campaign = models.ForeignKey(OutreachCampaign, on_delete=models.CASCADE, related_name="recipients")
    lead = models.ForeignKey('DiscoveredLead', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="pending")  # pending, sent, delivered, failed
    response = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.lead.address} - {self.campaign.name}"


# --- Lead Discovery Model ---
class DiscoveredLead(models.Model):
    SOURCE_CHOICES = [
        ('public_record', 'Public Record'),
        ('property_site', 'Property Site'),
        ('social_media', 'Social Media'),
        ('court_record', 'Court Record'),
        ('mls', 'MLS'),
    ]
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    details = models.TextField(blank=True, null=True)
    motivation_score = models.FloatField(default=0.0)
    property_condition = models.CharField(max_length=100, blank=True, null=True)
    financial_situation = models.CharField(max_length=100, blank=True, null=True)
    timeline_urgency = models.CharField(max_length=100, blank=True, null=True)
    negotiation_style = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address} ({self.source})"

# --- AI Performance Metrics Models ---
class VoiceAICallMetrics(models.Model):
    total_calls = models.IntegerField(default=0)
    success_rate = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Voice AI Calls: {self.total_calls} ({self.success_rate}%)"

class VisionAnalysisMetrics(models.Model):
    total_analyses = models.IntegerField(default=0)
    accuracy_rate = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Vision Analyses: {self.total_analyses} ({self.accuracy_rate}%)"
from django.db import models
import uuid

# 1. Core Business Metrics
class BusinessMetrics(models.Model):
    total_revenue = models.DecimalField(max_digits=18, decimal_places=2)
    active_users = models.IntegerField()
    properties_listed = models.IntegerField()
    ai_conversations = models.DecimalField(max_digits=18, decimal_places=2)
    total_deals = models.IntegerField()
    monthly_profit = models.DecimalField(max_digits=18, decimal_places=2)
    voice_calls_count = models.IntegerField()
    report_date = models.DateField()

    def __str__(self):
        return f"Metrics on {self.report_date}"


# 2. Historical Data
class HistoricalMetrics(models.Model):
    metric_type = models.CharField(max_length=50)   # e.g. revenue, active_users
    metric_value = models.DecimalField(max_digits=18, decimal_places=2)
    record_date = models.DateField()

    def __str__(self):
        return f"{self.metric_type} - {self.record_date}"


# 3. Real-Time Activity
class ActivityFeed(models.Model):
    user_id = models.IntegerField()
    action_type = models.CharField(max_length=100)  # e.g. deal_completed, login
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_type} by {self.user_id} at {self.timestamp}"


# 4. Compliance & System Health
class ComplianceStatus(models.Model):
    compliance_percent = models.DecimalField(max_digits=5, decimal_places=2)
    audit_trail = models.TextField()
    system_health = models.CharField(max_length=50)  # e.g. healthy, warning
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Compliance {self.compliance_percent}% ({self.system_health})"
    
class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    subscription_status = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=50, default="user")
    #role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    level = models.IntegerField(default=1)
    points = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relationship
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="users"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=150)

    def __str__(self):
        return self.label

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=150)
    permissions = models.ManyToManyField(Permission, related_name="roles")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label
    
class PropertyAIAnalysis(models.Model):
    address = models.CharField(max_length=255, unique=True)
    ai_confidence = models.FloatField()
    distress_level = models.FloatField()
    motivation = models.CharField(max_length=255)
    timeline = models.CharField(max_length=255)
    roi_percent = models.FloatField()
    cap_rate = models.FloatField()
    cash_flow = models.FloatField()
    market_stability_score = models.FloatField()
    comparables_confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address} AI Analysis"

class NLPProcessingMetrics(models.Model):
    total_processed = models.IntegerField(default=0)
    accuracy_rate = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"NLP Processed: {self.total_processed} ({self.accuracy_rate}%)"

class BlockchainTxnMetrics(models.Model):
    total_txns = models.IntegerField(default=0)
    success_rate = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Blockchain Txns: {self.total_txns} ({self.success_rate}%)"
    
class Campaign(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("paused", "Paused"),
        ("completed", "Completed"),
    ]

    CHANNEL_CHOICES = [
        ("email", "Email"),
        ("sms", "SMS"),
        ("call", "Call"),
    ]

    name = models.CharField(max_length=255)
    campaign_type = models.CharField(max_length=100, default="new")
    channel = models.CharField(max_length=500, default="[]", blank=True)   # store ["email", "sms", "phone"]
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)

    # Geographic Scope
    geographic_scope_type = models.CharField(max_length=50, default="zip", choices=[("zip", "Zip"), ("county", "County"), ("state", "State")])
    geographic_scope_values = models.CharField(max_length=500, default="[]", blank=True)   # store ["Miami-Dade", "Broward"]

    # Target Criteria
    location = models.CharField(max_length=255, null=True, blank=True)
    property_type = models.CharField(max_length=100, null=True, blank=True)
    minimum_equity = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Property Criteria
    min_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Distress Indicators
    distress_indicators = models.CharField(max_length=500, default="[]", blank=True)   # e.g. ["Pre-foreclosure", "Tax Liens"]

    # Email Content
    subject_line = models.CharField(max_length=500, null=True, blank=True)
    email_content = models.TextField(null=True, blank=True)

    # AI Features
    use_ai_personalization = models.BooleanField(default=False)

    # Seller Finder - Geographic Details
    seller_country = models.CharField(max_length=100, blank=True, null=True)
    seller_state = models.CharField(max_length=100, blank=True, null=True)
    seller_counties = models.CharField(max_length=100, blank=True, null=True)
    seller_city = models.CharField(max_length=100, blank=True, null=True)
    seller_districts = models.CharField(max_length=100, blank=True, null=True)
    seller_parish = models.CharField(max_length=100, blank=True, null=True)
    
    # Seller Finder - Additional Fields
    property_year_built_min = models.IntegerField(null=True, blank=True)
    property_year_built_max = models.IntegerField(null=True, blank=True)
    seller_keywords = models.CharField(max_length=500, blank=True, null=True)
    
    # Buyer Finder - Geographic Details
    buyer_country = models.CharField(max_length=100, blank=True, null=True)
    buyer_state = models.CharField(max_length=100, blank=True, null=True)
    buyer_counties = models.CharField(max_length=100, blank=True, null=True)
    buyer_city = models.CharField(max_length=100, blank=True, null=True)
    buyer_districts = models.CharField(max_length=100, blank=True, null=True)
    buyer_parish = models.CharField(max_length=100, blank=True, null=True)
    
    # Buyer Finder - Demographic Details
    last_qualification = models.CharField(max_length=100, blank=True, null=True)
    age_range = models.CharField(max_length=50, blank=True, null=True)
    ethnicity = models.CharField(max_length=100, blank=True, null=True)
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True)
    employment_status = models.CharField(max_length=100, blank=True, null=True)
    home_ownership_status = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Lead(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("qualified", "Qualified"),
        ("converted", "Converted"),
        ("contacted", "Contacted"),
        ("interested", "Interested"),
        ("not_interested", "Not Interested"),
    ]

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="leads", null=True, blank=True)
    name = models.CharField(max_length=255, default="Unknown Lead")
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    source = models.CharField(max_length=50, default='manual')
    motivation_score = models.FloatField(default=0.0)
    property_condition = models.CharField(max_length=100, blank=True, null=True)
    financial_situation = models.CharField(max_length=100, blank=True, null=True)
    timeline_urgency = models.CharField(max_length=100, blank=True, null=True)
    negotiation_style = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    responded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Lead {self.id} - {self.name} ({self.status})"


class Channel(models.Model):
    CHANNEL_CHOICES = [
        ("email", "Email"),
        ("sms", "SMS"),
        ("voice", "Voice"),
        ("whatsapp", "WhatsApp"),
    ]

    name = models.CharField(max_length=50, choices=CHANNEL_CHOICES, unique=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class CampaignPropertyStats(models.Model):
    total_properties = models.IntegerField()
    distressed_properties = models.IntegerField()
    competition_level = models.CharField(max_length=50)  # e.g., Low, Medium, High
    avg_roi = models.DecimalField(max_digits=6, decimal_places=2)  # percentage
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Properties: {self.total_properties}, ROI: {self.avg_roi}%"
    

class CampaignPerformance(models.Model):
    campaign_type = models.CharField(max_length=100)  # e.g., Heat Mapping, Social Media
    roi_percentage = models.DecimalField(max_digits=6, decimal_places=2)  # percentage
    date_range = models.CharField(max_length=100, default="Last 30 days")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.campaign_type}: {self.roi_percentage}%"


class ChannelResponseRate(models.Model):
    channel_name = models.CharField(max_length=100)  # e.g., Voice Calls, SMS, Email, WhatsApp
    response_rate = models.DecimalField(max_digits=6, decimal_places=2)  # percentage
    date_range = models.CharField(max_length=100, default="Last 30 days")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.channel_name}: {self.response_rate}%"


# --- Property Model ---
class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('land', 'Land'),
        ('industrial', 'Industrial'),
        ('condo', 'Condo'),
        ('townhouse', 'Townhouse'),
        ('apartment', 'Apartment'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('pending', 'Pending'),
        ('withdrawn', 'Withdrawn'),
        ('off_market', 'Off Market'),
    ]
    
    address = models.CharField(max_length=255)
    unit_apt = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    county = models.CharField(max_length=100, blank=True, null=True)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default='residential')
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.FloatField(null=True, blank=True)
    square_feet = models.IntegerField(null=True, blank=True)
    lot_size = models.FloatField(null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    images = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Financial fields
    arv = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # After Repair Value
    repair_estimate = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    holding_costs = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    transaction_type = models.CharField(max_length=50, blank=True, null=True)
    assignment_fee = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    seller_notes = models.TextField(blank=True, null=True)
    ai_analysis = models.ForeignKey('PropertyAIAnalysis', on_delete=models.SET_NULL, null=True, blank=True, related_name='property_analyses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.address} - ${self.price}"


# --- Deal Model ---
class Deal(models.Model):
    DEAL_TYPE_CHOICES = [
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
        ('lease', 'Lease'),
        ('investment', 'Investment'),
        ('wholesale', 'Wholesale'),
        ('flip', 'Flip'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='deals')
    buyer_lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='buyer_deals', null=True, blank=True)
    seller_lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='seller_deals', null=True, blank=True)
    deal_type = models.CharField(max_length=20, choices=DEAL_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    offer_price = models.DecimalField(max_digits=12, decimal_places=2)
    final_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    commission = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    closing_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Deal {self.id} - {self.property.address}"


# --- AI Analysis Model ---
class AIAnalysis(models.Model):
    ANALYSIS_TYPE_CHOICES = [
        ('property_condition', 'Property Condition'),
        ('market_analysis', 'Market Analysis'),
        ('lead_psychology', 'Lead Psychology'),
        ('sentiment_analysis', 'Sentiment Analysis'),
        ('price_prediction', 'Price Prediction'),
        ('investment_analysis', 'Investment Analysis'),
        ('neighborhood_analysis', 'Neighborhood Analysis'),
    ]
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True, related_name='ai_analyses')
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True, related_name='ai_analyses')
    analysis_type = models.CharField(max_length=50, choices=ANALYSIS_TYPE_CHOICES)
    result = models.JSONField()
    confidence_score = models.FloatField()
    processing_time = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.analysis_type} - {self.created_at}"


# --- Deal Milestone Model ---
class DealMilestone(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['due_date', 'created_at']
    
    def __str__(self):
        return f"{self.title} - {self.deal}"


# --- Saved Property Model ---
class SavedProperty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_properties')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='saved_by_users')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'property']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} saved {self.property.address}"


# --- Stripe Payment Gateway Models ---

# Stripe Subscription Package (Different pricing plans)
class SubscriptionPackage(models.Model):
    name = models.CharField(max_length=100)  # e.g. "Basic Plan", "Pro Plan"
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Price like 29.99
    currency = models.CharField(max_length=3, default='usd')
    interval = models.CharField(max_length=20)  # monthly, yearly
    stripe_product_id = models.CharField(max_length=100)  # Stripe's product ID
    stripe_price_id = models.CharField(max_length=100)    # Stripe's price ID
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ${self.amount}/{self.interval}"


# User Subscription (Who subscribed to what)
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Which user
    package = models.ForeignKey(SubscriptionPackage, on_delete=models.CASCADE)  # Which plan
    stripe_subscription_id = models.CharField(max_length=100)  # Stripe's subscription ID
    stripe_customer_id = models.CharField(max_length=100)     # Stripe's customer ID
    status = models.CharField(max_length=50)  # active, canceled, past_due
    current_period_end = models.DateTimeField(null=True, blank=True)
    card_last4 = models.CharField(max_length=4, blank=True)   # Last 4 digits of card
    card_brand = models.CharField(max_length=20, blank=True)  # visa, mastercard, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.package.name} ({self.status})"