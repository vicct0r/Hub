from django.contrib import admin
from .models import CD, Transaction, Order


@admin.register(CD)
class CDAdmin(admin.ModelAdmin):
    list_display = ['created', 'modified', 'is_active', 'last_conn', 'name', 'description', 'ip', 'region', 'balance']
    search_fields = ['created', 'is_active', 'name', 'ip', 'balance']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'supplier__name', 'buyer__name', 'product', 'quantity', 'total']
    search_fields = ['id', 'created_at', 'supplier__name', 'buyer__name', 'product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'client__name', 'seller__name']
    search_fields = ['id', 'created_at', 'client__name', 'seller__name']
