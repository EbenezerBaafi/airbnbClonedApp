from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from listings.models import Listing

class Booking(models.Model):
    """Model for property bookings"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    guest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.guest.username} - {self.listing.title} ({self.check_in} to {self.check_out})"
    
    def clean(self):
        """Validate booking dates"""
        if self.check_in >= self.check_out:
            raise ValidationError('Check-out date must be after check-in date.')
        
        if self.check_in < timezone.now().date():
            raise ValidationError('Check-in date cannot be in the past.')
        
        # Check for overlapping bookings
        overlapping = Booking.objects.filter(
            listing=self.listing,
            status__in=['pending', 'confirmed']
        ).exclude(pk=self.pk).filter(
            check_in__lt=self.check_out,
            check_out__gt=self.check_in
        )
        
        if overlapping.exists():
            raise ValidationError('This property is not available for the selected dates.')
    
    def save(self, *args, **kwargs):
        # Calculate total price
        if self.check_in and self.check_out:
            num_nights = (self.check_out - self.check_in).days
            self.total_price = num_nights * self.listing.price_per_night
        
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def num_nights(self):
        return (self.check_out - self.check_in).days
    
    @property
    def is_upcoming(self):
        return self.check_in > timezone.now().date()
    
    @property
    def is_active(self):
        today = timezone.now().date()
        return self.check_in <= today <= self.check_out
    
    class Meta:
        ordering = ['-created_at']