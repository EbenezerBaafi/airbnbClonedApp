from rest_framework import serializers
from users.models import User
from listings.models import Listing, ListingImage
from bookings.models import Booking
from reviews.models import Review

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'phone_number', 
                  'bio', 'profile_picture', 'is_verified', 'created_at']
        read_only_fields = ['id', 'created_at', 'is_verified']

class ListingImageSerializer(serializers.ModelSerializer):
    """Serializer for ListingImage model"""
    class Meta:
        model = ListingImage
        fields = ['id', 'image', 'caption', 'is_primary']

class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model"""
    host = UserSerializer(read_only=True)
    images = ListingImageSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    
    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['id', 'host', 'created_at', 'updated_at']

class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    guest = UserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    num_nights = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['id', 'guest', 'total_price', 'created_at', 'updated_at']

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""
    reviewer = UserSerializer(read_only=True)
    average_rating = serializers.ReadOnlyField()
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['id', 'reviewer', 'booking', 'listing', 'created_at', 'updated_at']