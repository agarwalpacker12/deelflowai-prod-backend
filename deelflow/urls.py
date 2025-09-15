    
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import create_user
#from .views import ChangePasswordView

urlpatterns = [
    # ...existing routes...
    path('api/property-ai-predictions/', views.get_property_ai_predictions, name='property_ai_predictions'),

    path("create-user/", create_user, name="create-user"),
    
    path('login/', views.login_user, name='login'),
    path('get_roles/', views.get_roles, name='get_roles'),
    path('create_role/', views.create_role, name='create_role'),
    path('delete_role/', views.delete_role, name='delete_role'),
    path('get_permissions/', views.get_permissions, name='get_permissions'),
    path('update_role_permissions/', views.update_role_permissions, name='update_role_permissions'),
    path('property_analysis/', views.property_analysis, name='property_analysis'),
    path('api/total-revenue/', views.get_total_revenue, name='total-revenue'),
    path('repair_analysis/', views.repair_analysis, name='repair_analysis'),
    path('recent_activity/', views.recent_activity, name='recent_activity'),
    path('api/active-users/', views.get_active_users, name='active-users'),
    path('neighborhood-analysis/', views.neighborhood_analysis, name='neighborhood-analysis'),
    path('market_comparables/', views.market_comparables, name='market_comparables'),
    path('api/properties-listed/', views.get_properties_listed, name='properties-listed'),

    path('api/ai-conversations/', views.get_ai_conversations, name='ai-conversations'),

    path('api/total-deals/', views.get_total_deals, name='total-deals'),

    path('api/monthly-profit/', views.get_monthly_profit, name='monthly-profit'),

    path('api/voice-calls-count/', views.get_voice_calls_count, name='voice-calls-count'),

    path('api/compliance-status/', views.get_compliance_status, name='compliance-status'),

    path('api/audit-trail-data/', views.get_audit_trail_data, name='audit-trail-data'),

    path('api/system-health-metrics/', views.get_system_health_metrics, name='system-health-metrics'),

    path('api/revenue-user-growth-chart-data/', views.get_revenue_user_growth_chart_data, name='revenue-user-growth-chart-data'),

    path('api/monthly-trend-data/', views.get_monthly_trend_data, name='monthly-trend-data'),

    path('api/historical-performance/', views.get_historical_performance, name='historical-performance'),

    path('api/live-activity-feed/', views.get_live_activity_feed, name='live-activity-feed'),

    path('api/user-actions-timestamps/', views.get_user_actions_timestamps, name='user-actions-timestamps'),

    path('api/deal-completions-scheduling/', views.get_deal_completions_scheduling, name='deal-completions-scheduling'),

    path('api/voice-calls-count/', views.get_voice_ai_call_metrics, name='voice_ai_call_metrics'),
    path('api/vision-analysis/', views.get_vision_analysis_metrics, name='vision_analysis_metrics'),
    path('api/nlp-processing/', views.get_nlp_processing_metrics, name='nlp_processing_metrics'),
    path('api/blockchain-txns/', views.get_blockchain_txns_metrics, name='blockchain_txns_metrics'),
    path('active_campaign_summary/', views.active_campaign_summary, name='active_campaign_summary'),
    path('lead_conversion_funnel/', views.lead_conversion_funnel, name='lead_conversion_funnel'),
    path('channel_status/', views.channel_status, name='channel_status'),
    path('campaign_property_stats/', views.campaign_property_stats, name='campaign_property_stats'),
    path('campaign_performance_overview/', views.campaign_performance_overview, name='campaign_performance_overview'),
    path('channel_response_rates/', views.channel_response_rates, name='channel_response_rates'),
    path('api/ai-metrics/overall-accuracy/', views.get_overall_accuracy, name='overall_accuracy'),
    path('api/market-alerts/recent/', views.recent_market_alerts, name='recent_market_alerts'),
]