from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Product, Order
from .serializers import ProductCreateSerializer, ProductListSerializer, OrderCreateSerializer, OrderListSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("supplier").all()

    def get_serializer_class(self):
        if self.action == "create":
            return ProductCreateSerializer
        return ProductListSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.select_related("user").prefetch_related("products").all()

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderListSerializer

