
# --- Required imports ---
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import VoiceAICallMetrics, VisionAnalysisMetrics
import requests
from twilio.rest import Client

# API view to get the latest overall AI accuracy
@api_view(['GET'])
def get_overall_accuracy(request):
    latest_metrics = VisionAnalysisMetrics.objects.order_by('-updated_at').first()
    previous_metrics = VisionAnalysisMetrics.objects.order_by('-updated_at')[1] if VisionAnalysisMetrics.objects.count() > 1 else None

    if latest_metrics:
        overall_accuracy = float(latest_metrics.accuracy_rate)
        percentage = 0
        if previous_metrics:
            previous_accuracy = float(previous_metrics.accuracy_rate)
            if previous_accuracy != 0:
                percentage = ((overall_accuracy - previous_accuracy) / previous_accuracy) * 100
        return Response({
            'overall_accuracy': f"{overall_accuracy}%",
            'change_percentage': round(percentage, 2)
        })
    return Response({'overall_accuracy': None, 'change_percentage': None})

# --- AI Performance Metrics via 3rd Party APIs ---

# Voice AI Calls
@api_view(['GET'])
def get_voice_ai_call_metrics(request):
    # Twilio credentials (replace with your actual credentials)
    account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
    auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
    client = Client(account_sid, auth_token)
    try:
        # Fetch call logs (example: last 30 days)
        from datetime import datetime, timedelta
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        calls = client.calls.list(start_time_after=start_date, start_time_before=end_date)
        total_calls = len(calls)
        successful_calls = sum(1 for call in calls if call.status == 'completed')
        success_rate = (successful_calls / total_calls * 100) if total_calls > 0 else 0.0
        # Use the latest call's timestamps for demo
        created_at = calls[0].start_time if calls else None
        updated_at = calls[0].end_time if calls else None
        return Response({
            'total_calls': total_calls,
            'success_rate': round(success_rate, 2),
            'created_at': created_at,
            'updated_at': updated_at
        })
    except Exception as e:
        # Fallback dummy data
        return Response({'total_calls': 0, 'success_rate': 0.0, 'error': str(e)})

# Vision Analysis
@api_view(['GET'])
def get_vision_analysis_metrics(request):
    try:
        response = requests.get('https://api.example.com/vision-analysis', timeout=5)  # Replace with real API
        if response.status_code == 200:
            data = response.json()
            return Response({
                'total_analyses': data.get('total_analyses', 0),
                'accuracy_rate': data.get('accuracy_rate', 0.0),
                'created_at': data.get('created_at'),
                'updated_at': data.get('updated_at')
            })
    except Exception as e:
        pass
    return Response({'total_analyses': 0, 'accuracy_rate': 0.0})

# NLP Processing
@api_view(['GET'])
def get_nlp_processing_metrics(request):
    try:
        response = requests.get('https://api.example.com/nlp-processing', timeout=5)  # Replace with real API
        if response.status_code == 200:
            data = response.json()
            return Response({
                'total_processed': data.get('total_processed', 0),
                'accuracy_rate': data.get('accuracy_rate', 0.0),
                'created_at': data.get('created_at'),
                'updated_at': data.get('updated_at')
            })
    except Exception as e:
        pass
    return Response({'total_processed': 0, 'accuracy_rate': 0.0})

# Blockchain Txns
@api_view(['GET'])
def get_blockchain_txns_metrics(request):
    try:
        response = requests.get('https://api.example.com/blockchain-txns', timeout=5)  # Replace with real API
        if response.status_code == 200:
            data = response.json()
            return Response({
                'total_txns': data.get('total_txns', 0),
                'success_rate': data.get('success_rate', 0.0),
                'created_at': data.get('created_at'),
                'updated_at': data.get('updated_at')
            })
    except Exception as e:
        pass
    return Response({'total_txns': 0, 'success_rate': 0.0})

from .models import PropertyAIAnalysis
# API view to get AI predictions for properties

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BusinessMetrics
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .decorators import unauthenticated_user,allowed_users,admin_only

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render
import io
from json.encoder import JSONEncoder
from logging import NullHandler
import locale
import re
import requests
import time
from typing import IO
from django.http import response
from django.views.decorators.csrf import ensure_csrf_cookie
import os
from datetime import datetime
from django.db import Error
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.http import HttpResponse
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.core.mail import EmailMessage
from django.core.mail import BadHeaderError, send_mail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.http.response import JsonResponse
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.template.loader import get_template, render_to_string
from django.template import Context
from django.http import HttpResponse
from html import escape
import datetime
from datetime import datetime

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from django.utils.decorators import decorator_from_middleware
from corsheaders.middleware import CorsMiddleware

import json
from rest_framework.parsers import JSONParser
from .serializers import UserSerializer
from rest_framework import status


from collections import defaultdict
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Role, Permission
from django.contrib.auth.hashers import check_password
from django.utils.timezone import localtime
from django.db import transaction


@api_view(["POST"])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_user(request):
    email = request.data.get("username")
    password = request.data.get("password")

    print("Attempting login for:", email)
    print("Attempting login for:", password)
    # Check if user exists
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"status": "error", "message": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Verify password
    if not check_password(password, user.password):
        return Response(
            {"status": "error", "message": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Generate JWT token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Custom response format
    data = {
        "status": "success",
        "message": "User logged in successfully",
        "data": {
            "token": access_token,
            "user": {
                "id": user.id,
                "uuid": str(user.uuid),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role
            }
        }
    }
    return Response(data, status=status.HTTP_200_OK)


# @csrf_exempt
# def loginpage(request):
#     if request.method == 'POST':
#         # Handle both JSON and form-data requests
#         if request.content_type == 'application/json':
#             try:
#                 data = json.loads(request.body.decode("utf-8"))
#                 username = data.get('username')
#                 password = data.get('password')
#             except Exception:
#                 return JsonResponse({"status": "Error", "result": {"response": "Invalid JSON format"}}, status=400)
#         else:
#             username = request.POST.get('username')
#             password = request.POST.get('password')

#         # Authenticate user
#         user = authenticate(request, username=username, password=password)
#         print("Authenticated user:", user)

#         if user is not None:
#             login(request, user)  # ✅ Django session created
#             return JsonResponse({"status": "Success", "result": {"response": "Login successful"}})
#         else:
#             return JsonResponse({"status": "Error", "result": {"response": "Username or Password is incorrect"}}, status=401)

#     return JsonResponse({"status": "Error", "result": {"response": "Only POST method allowed"}}, status=405)


# @csrf_exempt
# #@unauthenticated_user
# def loginpage(request):
#     if request.method == 'POST':
#         Username = request.POST.get('username')
#         Password = request.POST.get('password')

#         # Normal Django authentication
#         user = authenticate(request, username=Username, password=Password)
#         if user is not None:
#             login(request, user)
#             return redirect('user')
#             # If you want JsonResponse instead of redirect, keep below lines
#             # res = {"status": "Success", "result": {"responce": "login successful"}}
#             # return JsonResponse(res)
#         else:
#             res = {"status": "Error", "result": {"responce": "Username Or Password is Incorrect"}}
#             return JsonResponse(res)

#     return render(request, 'FDA/login.html')


# API view to get the latest total revenue
@api_view(['GET'])
def get_total_revenue(request):
    latest_metrics = BusinessMetrics.objects.order_by('-report_date').first()
    previous_metrics = BusinessMetrics.objects.order_by('-report_date')[1] if BusinessMetrics.objects.count() > 1 else None

    if latest_metrics:
        total_revenue = float(latest_metrics.total_revenue)
        percentage = 0
        if previous_metrics:
            previous_revenue = float(previous_metrics.total_revenue)
            if previous_revenue != 0:
                percentage = ((total_revenue - previous_revenue) / previous_revenue) * 100
        return Response({
            'total_revenue': str(total_revenue),
            'change_percentage': round(percentage, 2)
        })
    return Response({'total_revenue': None, 'percentage': None})

# API view to get the latest active users
@api_view(['GET'])
def get_active_users(request):
    from django.utils import timezone
    user_count = User.objects.count()
    today = timezone.now().date()
    users_added_today = User.objects.filter(created_at__date=today).count()
    percentage_today = (users_added_today / user_count * 100) if user_count > 0 else 0
    return Response({
        'active_users': user_count,
        'change_percentage': round(percentage_today, 2)
    })

# API view to get the latest properties listed
@api_view(['GET'])
def get_properties_listed(request):
	latest_metrics = BusinessMetrics.objects.order_by('-report_date').first()
	if latest_metrics:
		return Response({'properties_listed': latest_metrics.properties_listed})
	return Response({'properties_listed': None})

# API view to get the latest AI conversations
@api_view(['GET'])
def get_ai_conversations(request):
    latest_metrics = BusinessMetrics.objects.order_by('-report_date').first()
    previous_metrics = BusinessMetrics.objects.order_by('-report_date')[1] if BusinessMetrics.objects.count() > 1 else None

    if latest_metrics:
        ai_conversations = float(latest_metrics.ai_conversations)
        percentage = 0
        if previous_metrics:
            previous_ai_conversations = float(previous_metrics.ai_conversations)
            if previous_ai_conversations != 0:
                percentage = ((ai_conversations - previous_ai_conversations) / previous_ai_conversations) * 100
        return Response({
            'ai_conversations': str(ai_conversations),
            'change_percentage': round(percentage, 2)
        })
    return Response({'ai_conversations': None, 'change_percentage': None})

# API view to get the latest total deals
@api_view(['GET'])
def get_total_deals(request):
    latest_metrics = BusinessMetrics.objects.order_by('-report_date').first()
    previous_metrics = BusinessMetrics.objects.order_by('-report_date')[1] if BusinessMetrics.objects.count() > 1 else None

    if latest_metrics:
        total_deals = float(latest_metrics.total_deals)
        percentage = 0
        if previous_metrics:
            previous_deals = float(previous_metrics.total_deals)
            if previous_deals != 0:
                percentage = ((total_deals - previous_deals) / previous_deals) * 100
        return Response({
            'total_deals': str(total_deals),
            'change_percentage': round(percentage, 2)
        })
    return Response({'total_deals': None, 'change_percentage': None})

# API view to get the latest monthly profit
@api_view(['GET'])
def get_monthly_profit(request):
    latest_metrics = BusinessMetrics.objects.order_by('-report_date').first()
    previous_metrics = BusinessMetrics.objects.order_by('-report_date')[1] if BusinessMetrics.objects.count() > 1 else None

    if latest_metrics:
        monthly_profit = float(latest_metrics.monthly_profit)
        percentage = 0
        if previous_metrics:
            previous_monthly_profit = float(previous_metrics.monthly_profit)
            if previous_monthly_profit != 0:
                percentage = ((monthly_profit - previous_monthly_profit) / previous_monthly_profit) * 100
        return Response({
            'monthly_profit': str(monthly_profit),
            'change_percentage': round(percentage, 2)
        })
    return Response({'monthly_profit': None, 'change_percentage': None})

# API view to get the latest voice calls count
@api_view(['GET'])
def get_voice_calls_count(request):
    latest_metrics = BusinessMetrics.objects.order_by('-report_date').first()
    previous_metrics = BusinessMetrics.objects.order_by('-report_date')[1] if BusinessMetrics.objects.count() > 1 else None

    if latest_metrics:
        voice_calls_count = float(latest_metrics.voice_calls_count)
        percentage = 0
        if previous_metrics:
            previous_voice_calls_count = float(previous_metrics.voice_calls_count)
            if previous_voice_calls_count != 0:
                percentage = ((voice_calls_count - previous_voice_calls_count) / previous_voice_calls_count) * 100
        return Response({
            'voice_calls_count': str(voice_calls_count),
            'change_percentage': round(percentage, 2)
        })
    return Response({'voice_calls_count': None, 'change_percentage': None})

# API view to get the latest compliance status
@api_view(['GET'])
def get_compliance_status(request):
	from .models import ComplianceStatus
	latest_status = ComplianceStatus.objects.order_by('-updated_at').first()
	if latest_status:
		return Response({
			'compliance_percent': str(latest_status.compliance_percent),
			'audit_trail': latest_status.audit_trail,
			'system_health': latest_status.system_health,
			'updated_at': latest_status.updated_at
		})
	return Response({'compliance_percent': None, 'audit_trail': None, 'system_health': None, 'updated_at': None})

# API view to get the latest audit trail data
@api_view(['GET'])
def get_audit_trail_data(request):
	from .models import ComplianceStatus
	latest_status = ComplianceStatus.objects.order_by('-updated_at').first()
	if latest_status:
		return Response({'audit_trail': latest_status.audit_trail})
	return Response({'audit_trail': None})

# API view to get the latest system health metrics
@api_view(['GET'])
def get_system_health_metrics(request):
	from .models import ComplianceStatus
	latest_status = ComplianceStatus.objects.order_by('-updated_at').first()
	if latest_status:
		return Response({'system_health': latest_status.system_health})
	return Response({'system_health': None})

# API view to get revenue & user growth chart data
@api_view(['GET'])
def get_revenue_user_growth_chart_data(request):
	# from .models import HistoricalMetrics
    revenue_data = HistoricalMetrics.objects.filter(metric_type='revenue').order_by('record_date')
    user_data = HistoricalMetrics.objects.filter(metric_type='active_users').order_by('record_date')
    revenue_chart = [{'date': r.record_date, 'value': r.metric_value} for r in revenue_data]
    user_chart = [{'date': u.record_date, 'value': u.metric_value} for u in user_data]
    return Response({
        'revenue_chart': revenue_chart,
        'user_growth_chart': user_chart
    })

# API view to get monthly trend data
@api_view(['GET'])
def get_monthly_trend_data(request):
	from .models import HistoricalMetrics
	# Assuming 'monthly_trend' is a metric_type in HistoricalMetrics
	trend_data = HistoricalMetrics.objects.filter(metric_type='monthly_trend').order_by('date')
	trend_chart = [{'date': t.date, 'value': t.value} for t in trend_data]
	return Response({'monthly_trend_chart': trend_chart})

# API view to get historical performance data
@api_view(['GET'])
def get_historical_performance(request):
	from .models import HistoricalMetrics
	performance_data = HistoricalMetrics.objects.all().order_by('date')
	performance_chart = [
		{
			'date': p.date,
			'metric_type': p.metric_type,
			'value': p.value
		} for p in performance_data
	]
	return Response({'historical_performance': performance_chart})

# API view to get live activity feed
@api_view(['GET'])
def get_live_activity_feed(request):
	# from .models import ActivityFeed
    activities = ActivityFeed.objects.order_by('-timestamp')[:50]  # latest 50 activities
    feed = [
        {
            'user': getattr(a, 'user_name', None) or getattr(a, 'user_id', None) or '',
            'action_type': a.action_type,
            'description': a.description,
            'timestamp': a.timestamp
        }
        for a in activities
    ]
    return Response({'live_activity_feed': feed})

# API view to get user actions and timestamps
@api_view(['GET'])
def get_user_actions_timestamps(request):
	from .models import ActivityFeed
	activities = ActivityFeed.objects.order_by('-timestamp')[:50]
	actions = [
		{
			'user': a.user,
			'action_type': a.action_type,
			'timestamp': a.timestamp
		} for a in activities
	]
	return Response({'user_actions_timestamps': actions})

# API view to get deal completions and scheduling
@api_view(['GET'])
def get_deal_completions_scheduling(request):
	from .models import ActivityFeed
	completions = ActivityFeed.objects.filter(action_type='deal_completed').order_by('-timestamp')[:50]
	scheduling = ActivityFeed.objects.filter(action_type='deal_scheduled').order_by('-timestamp')[:50]
	completions_data = [
		{
			'user': c.user,
			'description': c.description,
			'timestamp': c.timestamp
		} for c in completions
	]
	scheduling_data = [
		{
			'user': s.user,
			'description': s.description,
			'timestamp': s.timestamp
		} for s in scheduling
	]
	return Response({
		'deal_completions': completions_data,
		'deal_scheduling': scheduling_data
	})
 

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def get_roles(request):
    try:
        user = request.user

        # Assuming user.role.name defines if it's super admin
        is_super_admin = hasattr(user, "role") and user.role.name.lower() == "super_admin"

        # Query roles
        if is_super_admin:
            roles = Role.objects.prefetch_related("permissions").all()
        else:
            roles = Role.objects.prefetch_related("permissions").exclude(name__iexact="super_admin")

        roles_data = []
        for role in roles:
            permissions_data = [
                {
                    "id": perm.id,
                    "name": perm.name,
                    "label": perm.label
                }
                for perm in role.permissions.all()
            ]

            role_data = {
                "id": role.id,
                "name": role.name,
                "label": role.label,
                "permissions": permissions_data,
                "created_at": localtime(role.created_at).isoformat(),
                "updated_at": localtime(role.updated_at).isoformat()
            }

            if is_super_admin:
                role_data["users_count"] = User.objects.filter(role=role).count()

            roles_data.append(role_data)

        response = {
            "status": "success",
            "message": "Roles retrieved successfully",
            "data": {
                "roles": roles_data,
                "total_roles": len(roles_data)
            }
        }
        return Response(response, status=200)

    except Exception as e:
        return Response(
            {
                "status": "error",
                "message": f"Failed to retrieve roles: {str(e)}"
            },
            status=500
        )
        

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def get_permissions(request):
    try:
        user = request.user

        # Check if user is super admin
        if not (hasattr(user, "role") and user.role.name.lower() == "super_admin"):
            return Response(
                {
                    "status": "success",
                    "message": "Access denied. You need super admin privileges to access permissions data.",
                    "error_code": "FORBIDDEN"
                },
                status=200
            )

        # Fetch all permissions with related roles
        permissions = Permission.objects.prefetch_related("roles").all()

        grouped_permissions = defaultdict(list)

        for perm in permissions:
            roles_data = [
                {
                    "id": role.id,
                    "name": role.name,
                    "label": role.label,
                    "enabled": role in perm.roles.all()
                }
                for role in Role.objects.all()
            ]

            permission_data = {
                "id": perm.id,
                "name": perm.name,
                "label": perm.label,
                "roles": roles_data,
                "created_at": localtime(perm.created_at).isoformat(),
                "updated_at": localtime(perm.updated_at).isoformat()
            }

            grouped_permissions[perm.group].append(permission_data)

        response = {
            "success": True,
            "status_code": 200,
            "message": "Permissions retrieved successfully",
            "data": {
                "permission_groups": [
                    {"group": group, "permissions": perms}
                    for group, perms in grouped_permissions.items()
                ],
                "total_permissions": permissions.count()
            }
        }
        return Response(response, status=200)

    except Exception as e:
        return Response(
            {
                "status": "error",
                "message": f"Failed to retrieve permissions: {str(e)}"
            },
            status=500
        )
        

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def update_role_permissions(request):
    try:
        user = request.user

        # ✅ Super Admin check
        if not (hasattr(user, "role") and user.role.name.lower() == "super_admin"):
            return Response(
                {
                    "status": "success",
                    "message": "Access denied. You need super admin privileges to update role permissions.",
                    "error_code": "FORBIDDEN"
                },
                status=200
            )

        # ✅ Get role_id from payload
        role_id = request.data.get("role_id")
        if not role_id:
            return Response(
                {
                    "status": "success",
                    "message": "Validation failed for updating role permissions",
                    "error_code": "VALIDATION_ERROR",
                    "errors": ["The role_id field is required."]
                },
                status=200
            )

        # ✅ Validate request body
        permissions_list = request.data.get("permissions")
        if permissions_list is None:
            return Response(
                {
                    "status": "success",
                    "message": "Validation failed for updating role permissions",
                    "error_code": "VALIDATION_ERROR",
                    "errors": ["The permissions field is required."]
                },
                status=200
            )
        if not isinstance(permissions_list, list) or not all(isinstance(p, str) for p in permissions_list):
            return Response(
                {
                    "status": "success",
                    "message": "Validation failed for updating role permissions",
                    "error_code": "VALIDATION_ERROR",
                    "errors": ["The permissions field must be a list of strings."]
                },
                status=200
            )

        # ✅ Check role exists
        try:
            role = Role.objects.get(pk=role_id)
        except Role.DoesNotExist:
            return Response(
                {"status": "success", "message": "Role not found", "error_code": "NOT_FOUND"},
                status=200
            )

        # ✅ Fetch valid permissions
        db_permissions = Permission.objects.filter(name__in=permissions_list)
        db_permission_names = set(db_permissions.values_list("name", flat=True))

        # ✅ Identify invalid ones
        invalid_permissions = [p for p in permissions_list if p not in db_permission_names]
        if invalid_permissions:
            return Response(
                {
                    "status": "success",
                    "message": "Some permissions do not exist",
                    "error_code": "INVALID_PERMISSIONS",
                    "details": {"requested_permissions": invalid_permissions},
                    "suggestions": [
                        "Ensure all permissions exist",
                        "Check permission names for typos"
                    ]
                },
                status=200
            )

        # ✅ Update inside a transaction
        with transaction.atomic():
            role.permissions.set(db_permissions)
            role.save()

        permissions_data = [
            {"id": perm.id, "name": perm.name, "label": perm.label}
            for perm in db_permissions
        ]

        response = {
            "status": "success",
            "message": "Role permissions updated successfully",
            "data": {
                "role_id": role.id,
                "role_name": role.name,
                "role_label": role.label,
                "permissions": permissions_data,
                "updated_at": localtime(role.updated_at).isoformat()
            }
        }
        return Response(response, status=200)

    except Exception as e:
        return Response(
            {"status": "success", "message": f"Failed to update role permissions: {str(e)}"},
            status=200
        )
        

# API view to create a new role
@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def create_role(request):
    """
    Create Role API
    POST /api/roles/create
    Payload: { "name": "manager", "label": "Manager", "permissions": ["perm1", "perm2"] }
    """
    try:
        name = request.data.get("name")
        label = request.data.get("label")
        permissions = request.data.get("permissions", [])

        # Validation
        if not name or not label:
            return Response({
                "status": "error",
                "message": "Validation failed for creating role",
                "error_code": "VALIDATION_ERROR",
                "errors": ["Both name and label fields are required."]
            }, status=400)

        # Check for duplicate role name
        if Role.objects.filter(name__iexact=name).exists():
            return Response({
                "status": "error",
                "message": "Role with this name already exists.",
                "error_code": "DUPLICATE_ROLE"
            }, status=400)

        with transaction.atomic():
            role = Role.objects.create(name=name, label=label)
            if permissions and isinstance(permissions, list):
                perms = Permission.objects.filter(name__in=permissions)
                role.permissions.set(perms)
            role.save()

        permissions_data = [
            {"id": perm.id, "name": perm.name, "label": perm.label}
            for perm in role.permissions.all()
        ]

        response = {
            "status": "success",
            "message": "Role created successfully",
            "data": {
                "id": role.id,
                "name": role.name,
                "label": role.label,
                "permissions": permissions_data,
                "created_at": localtime(role.created_at).isoformat(),
                "updated_at": localtime(role.updated_at).isoformat()
            }
        }
        return Response(response, status=201)

    except Exception as e:
        return Response(
            {"status": "error", "message": f"Failed to create role: {str(e)}"},
            status=500
        )
        

@api_view(['POST'])
def delete_role(request):
    try:
        user = request.user

        # ✅ Only Super Admin can delete roles
        if not (hasattr(user, "role") and user.role.name.lower() == "super_admin"):
            return Response(
                {
                    "status": "success",
                    "message": "Access denied. Super admin privileges required.",
                    "error_code": "FORBIDDEN"
                },
                status=200
            )

        # ✅ Validate payload
        role_id = request.data.get("role_id")
        if not role_id:
            return Response(
                {
                    "status": "success",
                    "message": "Validation failed",
                    "error_code": "VALIDATION_ERROR",
                    "errors": ["The role_id field is required."]
                },
                status=200
            )

        # ✅ Check if role exists
        try:
            role = Role.objects.get(pk=role_id)
        except Role.DoesNotExist:
            return Response(
                {"status": "success", "message": "Role not found", "error_code": "NOT_FOUND"},
                status=200
            )

        # ✅ Prevent deleting super_admin itself
        if role.name.lower() == "super_admin":
            return Response(
                {
                    "status": "success",
                    "message": "The super_admin role cannot be deleted.",
                    "error_code": "ROLE_PROTECTED"
                },
                status=200
            )

        # ✅ Perform deletion inside transaction
        with transaction.atomic():
            role.delete()

        return Response(
            {
                "status": "success",
                "message": f"Role '{role.name}' deleted successfully",
                "data": {"role_id": role_id}
            },
            status=200
        )

    except Exception as e:
        return Response(
            {"status": "success", "message": f"Failed to delete role: {str(e)}"},
            status=200
        )
        

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def property_analysis(request):
    """
    Property Analysis API
    POST /api/properties/analysis
    Payload: { "address": "1247 Oak Street, Dallas, TX 75201" }
    """

    address = request.data.get("address")

    # ✅ Validation
    if not address:
        return Response({
            "status": "error",
            "message": "Validation failed for property analysis",
            "error_code": "VALIDATION_ERROR",
            "errors": ["The address field is required."]
        }, status=400)

    # ⚡ For now we mock factual values (later you can fetch from DB or calculation service)
    if address == "1247 Oak Street, Dallas, TX 75201":
        analysis_data = {
            "address": address,
            "lot_price": 85000,
            "estimated_arv": 158000,
            "repair_estimate": 23000,
            "cash_investor_max_offer": 38500,
            "market_info": {
                "open_markets": 4,
                "price_reductions": 2,
                "last_updated": datetime.utcnow().isoformat() + "Z"
            }
        }
    else:
        return Response({
            "status": "error",
            "message": "Property data not found",
            "error_code": "PROPERTY_NOT_FOUND",
            "details": {
                "requested_address": address
            },
            "suggestions": [
                "Verify the property address",
                "Try searching with a property ID"
            ]
        }, status=404)

    # ✅ Success response
    return Response({
        "status": "success",
        "message": "Property analysis generated successfully",
        "data": analysis_data
    }, status=200)
    

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def repair_analysis(request):
    """
    Repair Analysis API
    POST /api/properties/repairs
    Payload: { "property_id": 101 } OR { "address": "1247 Oak Street, Dallas, TX 75201" }
    """

    property_id = request.data.get("property_id")
    address = request.data.get("address")

    # ✅ Validation
    if not property_id and not address:
        return Response({
            "status": "error",
            "message": "Validation failed for repair analysis",
            "error_code": "VALIDATION_ERROR",
            "errors": ["Either property_id or address is required."]
        }, status=400)

    # ⚡ Mock dataset (later can be fetched from DB or inspection system)
    repairs_data = {
        "HVAC": 4500,
        "Plumbing": 2200,
        "Electrical": 1700,
        "Roofing": 6500,
        "Flooring": 4000,
        "Kitchen": 5200
    }

    total_estimate = sum(repairs_data.values())

    # ✅ Success response
    return Response({
        "status": "success",
        "message": "Repair analysis generated successfully",
        "data": {
            "property_id": property_id,
            "address": address,
            "repairs": repairs_data,
            "total_estimate": total_estimate
        }
    }, status=200)
    

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def recent_activity(request):
    """
    Recent Activity API
    POST /api/properties/activity
    Payload: { "property_id": 101 } OR { "address": "1247 Oak Street, Dallas, TX 75201" }
    """

    property_id = request.data.get("property_id")
    address = request.data.get("address")

    # ✅ Validation
    if not property_id and not address:
        return Response({
            "status": "error",
            "message": "Validation failed for recent activity",
            "error_code": "VALIDATION_ERROR",
            "errors": ["Either property_id or address is required."]
        }, status=400)

    # ⚡ Mock dataset (later can be plugged into CRM/MLS history data)
    activities = [
        {"event": "Price reduced by $3,000", "date": "2025-06-10"},
        {"event": "New roof installed", "date": "2025-04-22"},
        {"event": "HVAC system serviced", "date": "2025-02-15"},
        {"event": "Listed for sale 18 months ago", "date": "2024-03-01"}
    ]

    # ✅ Success response
    return Response({
        "status": "success",
        "message": "Recent activity retrieved successfully",
        "data": {
            "property_id": property_id,
            "address": address,
            "activities": activities,
            "last_updated": datetime.utcnow().isoformat() + "Z"
        }
    }, status=200)


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def neighborhood_analysis(request):
    """
    Neighborhood Analysis API
    POST /api/properties/neighborhood
    Payload: { "property_id": 101 } OR { "address": "1247 Oak Street, Dallas, TX 75201" }
    """

    property_id = request.data.get("property_id")
    address = request.data.get("address")

    # ✅ Validation
    if not property_id and not address:
        return Response({
            "status": "error",
            "message": "Validation failed for neighborhood analysis",
            "error_code": "VALIDATION_ERROR",
            "errors": ["Either property_id or address is required."]
        }, status=400)

    # ⚡ Mock data (later can integrate external APIs or DB)
    neighborhood_data = {
        "appreciation": "3.2%",
        "crime_rate": "Low",
        "school_rating": "Medium"
    }

    # ✅ Success response
    return Response({
        "status": "success",
        "message": "Neighborhood analysis retrieved successfully",
        "data": {
            "property_id": property_id,
            "address": address,
            "neighborhood_metrics": neighborhood_data,
            "last_updated": datetime.utcnow().isoformat() + "Z"
        }
    }, status=200)
    

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def market_comparables(request):
    """
    Market Comparables API
    POST /api/properties/comparables
    Payload: { "property_id": 101 } OR { "address": "1247 Oak Street, Dallas, TX 75201" }
    """

    property_id = request.data.get("property_id")
    address = request.data.get("address")

    # ✅ Validation
    if not property_id and not address:
        return Response({
            "status": "error",
            "message": "Validation failed for market comparables",
            "error_code": "VALIDATION_ERROR",
            "errors": ["Either property_id or address is required."]
        }, status=400)

    # ⚡ Mock dataset (later can be replaced with real MLS/DB comparables)
    comparables = {
        "similar_properties_count": 12,
        "examples": [
            {"address": "1250 Oak Street, Dallas, TX 75201", "price": 152000, "beds": 3, "baths": 2, "sqft": 1400},
            {"address": "1240 Pine Street, Dallas, TX 75201", "price": 160000, "beds": 4, "baths": 2, "sqft": 1550}
        ]
    }

    # ✅ Success response
    return Response({
        "status": "success",
        "message": "Market comparables retrieved successfully",
        "data": {
            "property_id": property_id,
            "address": address,
            "comparables": comparables,
            "last_updated": datetime.utcnow().isoformat() + "Z"
        }
    }, status=200)

@api_view(['GET'])
def get_property_ai_predictions(request):
    predictions = PropertyAIAnalysis.objects.all()
    data = []
    for p in predictions:
        data.append({
            'address': p.address,
            'ai_confidence': p.ai_confidence,
            'distress_level': p.distress_level,
            'motivation': p.motivation,
            'timeline': p.timeline,
            'roi_percent': p.roi_percent,
            'cap_rate': p.cap_rate,
            'cash_flow': p.cash_flow,
            'market_stability_score': p.market_stability_score,
            'comparables_confidence': p.comparables_confidence,
            'created_at': p.created_at,
            'updated_at': p.updated_at
        })
    return Response({'predictions': data})

# API view for NLP Processing Metrics
@api_view(['GET'])
def get_nlp_processing_metrics(request):
    from .models import NLPProcessingMetrics
    latest = NLPProcessingMetrics.objects.order_by('-updated_at').first()
    if latest:
        return Response({
            'total_processed': latest.total_processed,
            'accuracy_rate': latest.accuracy_rate,
            'created_at': latest.created_at,
            'updated_at': latest.updated_at
        })
    return Response({'total_processed': 0, 'accuracy_rate': 0.0})

# API view for Blockchain Transaction Metrics
@api_view(['GET'])
def get_blockchain_txns_metrics(request):
    from .models import BlockchainTxnMetrics
    latest = BlockchainTxnMetrics.objects.order_by('-updated_at').first()
    if latest:
        return Response({
            'total_txns': latest.total_txns,
            'success_rate': latest.success_rate,
            'created_at': latest.created_at,
            'updated_at': latest.updated_at
        })
    return Response({'total_txns': 0, 'success_rate': 0.0})


@api_view(['GET'])
def active_campaign_summary(request):
    try:
        total_active = Campaign.objects.filter(status="active").count()
        leads_today = Lead.objects.filter(created_at__date=timezone.now().date()).count()
        response_rate = Lead.objects.filter(responded=True).count() / Lead.objects.count() * 100 if Lead.objects.exists() else 0

        response = {
            "status": "success",
            "data": {
                "total_active": total_active,
                "leads_today": leads_today,
                "leads_today_change_pct": 23,  # Optional: computed from history
                "response_rate": round(response_rate, 2)
            }
        }
        return Response(response, status=200)
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=500)
    

@api_view(['GET'])
def lead_conversion_funnel(request):
    try:
        leads = Lead.objects.count()
        qualified = Lead.objects.filter(status="qualified").count()
        converted = Lead.objects.filter(status="converted").count()

        response = {
            "status": "success",
            "data": {
                "leads": leads,
                "qualified": qualified,
                "converted": converted
            }
        }
        return Response(response, status=200)
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=500)
    

@api_view(['GET'])
def channel_status(request):
    try:
        channels = {
            "email": "active" if Channel.objects.filter(name="email", active=True).exists() else "inactive",
            "sms": "active" if Channel.objects.filter(name="sms", active=True).exists() else "inactive",
            "voice": "active" if Channel.objects.filter(name="voice", active=True).exists() else "inactive",
            "whatsapp": "active" if Channel.objects.filter(name="whatsapp", active=True).exists() else "setup"
        }

        return Response({"status": "success", "data": channels}, status=200)
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=500)
    

@api_view(["GET"]) 
def campaign_property_stats(request):
    try:
        stats = CampaignPropertyStats.objects.latest("updated_at")

        response = {
            "status": "success",
            "message": "Campaign property stats retrieved successfully",
            "data": {
                "total_properties": stats.total_properties,
                "distressed_properties": stats.distressed_properties,
                "competition_level": stats.competition_level,
                "avg_roi": float(stats.avg_roi),
                "last_updated": localtime(stats.updated_at).isoformat()
            }
        }
        return Response(response, status=200)

    except CampaignPropertyStats.DoesNotExist:
        # ✅ Return 0 values instead of error
        response = {
            "status": "success",
            "message": "No campaign property stats found. Returning default values.",
            "data": {
                "total_properties": 0,
                "distressed_properties": 0,
                "competition_level": "N/A",
                "avg_roi": 0.0,
                "last_updated": None
            }
        }
        return Response(response, status=200)


@api_view(["GET"])
def campaign_performance_overview(request):
    try:
        performances = CampaignPerformance.objects.all()

        performance_data = [
            {
                "campaign_type": p.campaign_type,
                "roi_percentage": float(p.roi_percentage),
                "date_range": p.date_range,
                "last_updated": localtime(p.updated_at).isoformat()
            }
            for p in performances
        ]

        response = {
            "status": "success",
            "message": "Campaign performance overview retrieved successfully",
            "data": performance_data
        }
        return Response(response, status=200)
    except Exception as e:
        return Response(
            {"status": "success", "message": f"Failed to fetch campaign performance: {str(e)}"},
            status=200
        )
        
        
@api_view(["GET"])
def channel_response_rates(request):
    try:
        channels = ChannelResponseRate.objects.all()

        channel_data = [
            {
                "channel_name": c.channel_name,
                "response_rate": float(c.response_rate),
                "date_range": c.date_range,
                "last_updated": localtime(c.updated_at).isoformat()
            }
            for c in channels
        ]

        response = {
            "status": "success",
            "message": "Channel response rates retrieved successfully",
            "data": channel_data
        }
        return Response(response, status=200)
    except Exception as e:
        return Response(
            {"status": "success", "message": f"Failed to fetch channel response rates: {str(e)}"},
            status=200
        )
# API view to get recent market alerts
@api_view(['GET'])
def recent_market_alerts(request):
    # Mocked recent market alerts data
    alerts = [
        {
            "id": 1,
            "type": "price_drop",
            "message": "Property at 1247 Oak Street dropped price by 5%.",
            "timestamp": "2025-09-15T10:30:00Z"
        },
        {
            "id": 2,
            "type": "new_listing",
            "message": "New property listed in Dallas, TX.",
            "timestamp": "2025-09-15T09:00:00Z"
        },
        {
            "id": 3,
            "type": "market_trend",
            "message": "Dallas market shows increased buyer activity.",
            "timestamp": "2025-09-14T18:45:00Z"
        }
    ]
    return Response({
        "status": "success",
        "alerts": alerts
    })