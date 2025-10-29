from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model"""
    list_display = ['username', 'email', 'user_type', 'is_verified', 'is_staff', 'created_at']
    list_filter = ['user_type', 'is_verified', 'is_staff', 'is_superuser', 'created_at']
    search_fields = ['username', 'email', 'phone_number']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'bio', 'profile_picture', 
                      'date_of_birth', 'is_verified')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'user_type', 'phone_number')
        }),
    )