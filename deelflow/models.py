

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
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default="email")
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

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Lead(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("qualified", "Qualified"),
        ("converted", "Converted"),
    ]

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="leads")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    responded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lead {self.id} - {self.status}"


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