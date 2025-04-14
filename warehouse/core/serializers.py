from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from warehouse.core.models import Product, Order, OrderItem
from warehouse.users.api.serializers import SupplierListSerializer
from warehouse.users.models import Supplier, User
from warehouse.users.api.serializers import UserSerializer


class ProductCreateSerializer(serializers.ModelSerializer):
    supplier_id = serializers.IntegerField(required=True, label=_("Supplier ID"))
    class Meta:
        model = Product
        fields = ["product_name", "cost", "description", "total_quantity", "supplier_id"]

    def create(self, validated_data):
        supplier_id = validated_data.pop("supplier_id")
        supplier = Supplier.objects.filter(id=supplier_id).first()
        if not supplier:
            raise serializers.ValidationError({"supplier_id": "Supplier not found"})
        validated_data["supplier"] = supplier
        return super().create(validated_data)



class ProductListSerializer(serializers.ModelSerializer):
    supplier = SupplierListSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ["id", "product_name", "cost", "description", "total_quantity","supplier"]


class OrderItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True, label=_("Product ID"))
    quantity = serializers.IntegerField(required=True, label=_("Quantity"))


class OrderCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True, label=_("User ID"))
    items = OrderItemSerializer(many=True, label=_("Products"), required=True)
    class Meta:
        model = Order
        fields = ["user_id", "items"]

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise serializers.ValidationError({"user_id": "User not found"})
        validated_data["user"] = user
        products_data = validated_data.pop("items")
        order = Order.objects.create(user=user)
        for product_data in products_data:
            product_id = product_data.pop("product_id")
            product = Product.objects.filter(id=product_id).first()
            if not product:
                raise serializers.ValidationError({"product_id": "Product not found"})
            quantity = product_data.pop("quantity")
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
        return order


class OrderItemListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.product_name", read_only=True)
    cost = serializers.DecimalField(source="product.cost", max_digits=20, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["product_name", "cost", "quantity"]

class OrderListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = OrderItemListSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ["id", "user", "items", "date_created", "is_confirmed"]
