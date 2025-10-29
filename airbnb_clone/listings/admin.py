from django.contrib import admin
from .models import Listing, ListingImage

class ListingImageInline(admin.TabularInline):
    """Inline for listing images"""
    model = ListingImage
    extra = 1
    fields = ['image', 'caption', 'is_primary']

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    """Admin interface for Listing model"""
    list_display = ['title', 'host', 'property_type', 'city', 'country', 
                   'price_per_night', 'is_active', 'created_at']
    list_filter = ['property_type', 'is_active', 'city', 'country', 'created_at']
    search_fields = ['title', 'description', 'city', 'country', 'host__username']
    list_editable = ['is_active']
    date_hierarchy = 'created_at'
    inlines = [ListingImageInline]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('host', 'title', 'description', 'property_type')
        }),
        ('Location', {
            'fields': ('street_address', 'city', 'state', 'country', 'zip_code', 
                      'latitude', 'longitude')
        }),
        ('Property Details', {
            'fields': ('bedrooms', 'bathrooms', 'guests', 'price_per_night')
        }),
        ('Amenities', {
            'fields': ('wifi', 'kitchen', 'parking', 'air_conditioning', 
                      'heating', 'tv', 'pool', 'gym')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    """Admin interface for ListingImage model"""
    list_display = ['listing', 'is_primary', 'uploaded_at']
    list_filter = ['is_primary', 'uploaded_at']
    search_fields = ['listing__title', 'caption']