from django.contrib import admin

from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_filter = ('total_quantity', 'supplier__supplier_name',)
    search_fields = ('product_name',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    autocomplete_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_created', 'is_confirmed']
    inlines = [OrderItemInline]
    list_filter = ['is_confirmed', 'date_created']
    search_fields = ['user__username']
