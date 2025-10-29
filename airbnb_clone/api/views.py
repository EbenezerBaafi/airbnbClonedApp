from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from users.models import User
from listings.models import Listing
from bookings.models import Booking
from reviews.models import Review
from .serializers import (
    UserSerializer, ListingSerializer, 
    BookingSerializer, ReviewSerializer
)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class ListingViewSet(viewsets.ModelViewSet):
    """API endpoint for listings"""
    queryset = Listing.objects.filter(is_active=True)
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['property_type', 'city', 'country', 'bedrooms', 'bathrooms']
    search_fields = ['title', 'description', 'city', 'country']
    ordering_fields = ['price_per_night', 'created_at']
    
    def perform_create(self, serializer):
        serializer.save(host=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_listings(self, request):
        """Get current user's listings"""
        listings = self.queryset.filter(host=request.user)
        serializer = self.get_serializer(listings, many=True)
        return Response(serializer.data)

class BookingViewSet(viewsets.ModelViewSet):
    """API endpoint for bookings"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(guest=user) | Booking.objects.filter(listing__host=user)
    
    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        if booking.guest != request.user:
            return Response(
                {'error': 'You can only cancel your own bookings'},
                status=status.HTTP_403_FORBIDDEN
            )
        if booking.status not in ['pending', 'confirmed']:
            return Response(
                {'error': 'This booking cannot be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        booking.status = 'cancelled'
        booking.save()
        return Response({'status': 'booking cancelled'})
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a booking (host only)"""
        booking = self.get_object()
        if booking.listing.host != request.user:
            return Response(
                {'error': 'Only the host can confirm bookings'},
                status=status.HTTP_403_FORBIDDEN
            )
        if booking.status != 'pending':
            return Response(
                {'error': 'This booking cannot be confirmed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        booking.status = 'confirmed'
        booking.save()
        return Response({'status': 'booking confirmed'})

class ReviewViewSet(viewsets.ModelViewSet):
    """API endpoint for reviews"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)