from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin interface for Booking model"""
    list_display = ['id', 'guest', 'listing', 'check_in', 'check_out', 
                   'guests', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'check_in', 'check_out', 'created_at']
    search_fields = ['guest__username', 'listing__title', 'id']
    list_editable = ['status']
    date_hierarchy = 'check_in'
    
    fieldsets = (
        ('Booking Info', {
            'fields': ('guest', 'listing', 'check_in', 'check_out', 'guests')
        }),
        ('Payment', {
            'fields': ('total_price',)
        }),
        ('Status', {
            'fields': ('status', 'special_requests')
        }),
    )
    
    readonly_fields = ['total_price']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ['guest', 'listing']
        return self.readonly_fields