from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_email', 'city', 'region', 'zipcode', 'created_at')
    list_filter = ('region',)
    search_fields = ('customer_name', 'customer_email')
