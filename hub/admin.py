from django.contrib import admin
from .models import CD, Transaction


@admin.register(CD)
class CDAdmin(admin.ModelAdmin):
    list_display = ['last_conn', 'name', 'description', 'ip', 'region', 'balance']
    search_fields = ['name', 'ip', 'balance']


@admin.register
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'supplier', 'buyer', 'product', 'quantity', 'total']
    search_fields = ['id', 'created_at', 'supplier', 'buyer', 'product']