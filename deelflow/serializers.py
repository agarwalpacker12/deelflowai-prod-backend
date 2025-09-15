from rest_framework import serializers
from .models import BusinessMetrics, User, Organization
from django.contrib.auth.hashers import make_password
import uuid

class BusinessMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessMetrics
        fields = ['total_revenue', 'report_date']
        
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "uuid", "name", "slug", "subscription_status", "created_at", "updated_at"]


class UserSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = User
        fields = [
            "id", "uuid", "email", "first_name", "last_name",
            "phone", "role", "level", "points",
            "is_verified", "is_active", "stripe_customer_id",
            "password",   # 👈 include password
            "created_at", "updated_at", "organization"
        ]
        extra_kwargs = {
            "password": {"write_only": True}  # don’t return password in API
        }

    def create(self, validated_data):
        org_data = validated_data.pop("organization", None)
        raw_password = validated_data.pop("password", None)

        # hash the password
        if raw_password:
            validated_data["password"] = make_password(raw_password)

        # handle organization
        if org_data:
            org_uuid = org_data.get("uuid", str(uuid.uuid4()))
            organization, created = Organization.objects.get_or_create(
                uuid=org_uuid,
                defaults={
                    "name": org_data.get("name"),
                    "slug": org_data.get("slug"),
                    "subscription_status": org_data.get("subscription_status", "new"),
                }
            )
        else:
            organization = None

        user = User.objects.create(organization=organization, **validated_data)
        return user
