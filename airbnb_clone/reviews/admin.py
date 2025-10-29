from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin interface for Review model"""
    list_display = ['reviewer', 'listing', 'rating', 'average_rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['reviewer__username', 'listing__title', 'comment']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Review Info', {
            'fields': ('booking', 'listing', 'reviewer')
        }),
        ('Ratings', {
            'fields': ('rating', 'cleanliness', 'communication', 'check_in', 
                      'accuracy', 'location', 'value')
        }),
        ('Comments', {
            'fields': ('comment', 'host_response')
        }),
    )
    
    readonly_fields = ['booking', 'listing', 'reviewer']