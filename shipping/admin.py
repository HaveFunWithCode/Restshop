from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['shipping_status','created_at','customer']
    list_filter=['shipping_status']
    ordering = ['created_at']