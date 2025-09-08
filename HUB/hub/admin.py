from django.contrib import admin
from .models import CD


@admin.register(CD)
class CDAdmin(admin.ModelAdmin):
    list_display = ['created', 'modified', 'is_active', 'last_conn', 'name', 'description', 'ip', 'region', 'balance']
    search_fields = ['created', 'is_active', 'name', 'ip', 'balance']