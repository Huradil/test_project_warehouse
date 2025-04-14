from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from warehouse.users.models import User, Supplier


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "last_name", "first_name", "fullname", "email"]


class SupplierCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True, label=_("User id for supplier"))
    class Meta:
        model = Supplier
        fields = ["user_id","supplier_name", "website", "email", "phone_number"]

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        user = User.objects.filter(id=user_id).first()
        if user is None:
            raise serializers.ValidationError({"user_id": "User not found"})
        validated_data["user"] = user
        return super().create(validated_data)


class SupplierListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Supplier
        fields = "__all__"

