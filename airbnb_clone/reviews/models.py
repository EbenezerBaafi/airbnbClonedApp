from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from listings.models import Listing
from bookings.models import Booking

class Review(models.Model):
    """Model for property reviews"""
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    cleanliness = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    communication = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    check_in = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    accuracy = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    location = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    comment = models.TextField()
    host_response = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.listing.title}"
    
    @property
    def average_rating(self):
        return (self.cleanliness + self.communication + self.check_in + 
                self.accuracy + self.location + self.value) / 6
    
    class Meta:
        ordering = ['-created_at']