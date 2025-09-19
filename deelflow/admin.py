from .models import OutreachCampaign, CampaignRecipient




from django.contrib import admin
from .models import (
    BusinessMetrics, HistoricalMetrics, ActivityFeed,
    ComplianceStatus, User, Organization
)
from .models import (
    VoiceAICallMetrics,
    VisionAnalysisMetrics,
    Permission,
    Role,
    PropertyAIAnalysis,
    NLPProcessingMetrics,
    BlockchainTxnMetrics,
    Campaign,
    Lead,
    Channel,
    ChannelResponseRate,
    CampaignPerformance,
    CampaignPropertyStats,
)

admin.site.site_header = "DeelFlow Administration"
admin.site.site_title = "DeelFlow Admin Portal"
admin.site.index_title = "Welcome to DeelFlow Dashboard"
@admin.register(OutreachCampaign)
class OutreachCampaignAdmin(admin.ModelAdmin):
    list_display = ("name", "channel", "scheduled_time", "created_at")
    search_fields = ("name", "description")
    list_filter = ("channel",)

@admin.register(CampaignRecipient)
class CampaignRecipientAdmin(admin.ModelAdmin):
    list_display = ("campaign", "lead", "status", "sent_at")
    search_fields = ("lead__address", "campaign__name")
    list_filter = ("status", "campaign")
from .models import DiscoveredLead

@admin.register(DiscoveredLead)
class DiscoveredLeadAdmin(admin.ModelAdmin):
    list_display = ("address", "owner_name", "source", "motivation_score", "created_at")
    search_fields = ("address", "owner_name", "city", "state", "zipcode")
    list_filter = ("source", "state")

@admin.register(BusinessMetrics)
class BusinessMetricsAdmin(admin.ModelAdmin):
    list_display = ("report_date", "total_revenue", "active_users", "total_deals")

@admin.register(HistoricalMetrics)
class HistoricalMetricsAdmin(admin.ModelAdmin):
    list_display = ("metric_type", "metric_value", "record_date")

@admin.register(ActivityFeed)
class ActivityFeedAdmin(admin.ModelAdmin):
    list_display = ("user_id", "action_type", "timestamp")

@admin.register(ComplianceStatus)
class ComplianceStatusAdmin(admin.ModelAdmin):
    list_display = ("compliance_percent", "system_health", "updated_at")
    
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "uuid", "name", "slug", "subscription_status", "created_at", "updated_at")
    search_fields = ("name", "slug", "uuid")
    list_filter = ("subscription_status", "created_at")

@admin.register(VoiceAICallMetrics)
class VoiceAICallMetricsAdmin(admin.ModelAdmin):
    pass

@admin.register(VisionAnalysisMetrics)
class VisionAnalysisMetricsAdmin(admin.ModelAdmin):
    pass

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass

@admin.register(PropertyAIAnalysis)
class PropertyAIAnalysisAdmin(admin.ModelAdmin):
    pass

@admin.register(NLPProcessingMetrics)
class NLPProcessingMetricsAdmin(admin.ModelAdmin):
    pass

@admin.register(BlockchainTxnMetrics)
class BlockchainTxnMetricsAdmin(admin.ModelAdmin):
    pass

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    pass

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    pass

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    pass

@admin.register(ChannelResponseRate)
class ChannelResponseRateAdmin(admin.ModelAdmin):
    pass

@admin.register(CampaignPerformance)
class CampaignPerformanceAdmin(admin.ModelAdmin):
    pass

@admin.register(CampaignPropertyStats)
class CampaignPropertyStatsAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id", "uuid", "email", "first_name", "last_name", "phone",
        "role", "level", "points", "is_verified", "is_active",
        "organization", "created_at", "updated_at"
    )
    search_fields = ("email", "first_name", "last_name", "phone", "uuid")
    list_filter = ("role", "is_verified", "is_active", "organization", "created_at")
    ordering = ("-created_at",)
