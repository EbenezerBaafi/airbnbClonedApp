from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from .models import Booking
from .forms import BookingForm
from listings.models import Listing

@login_required
def create_booking(request, listing_pk):
    """View for creating a new booking"""
    listing = get_object_or_404(Listing, pk=listing_pk, is_active=True)
    
    # Check if user is not the host
    if request.user == listing.host:
        messages.error(request, 'You cannot book your own property.')
        return redirect('listing_detail', pk=listing_pk)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, listing=listing)
        if form.is_valid():
            try:
                booking = form.save(commit=False)
                booking.guest = request.user
                booking.listing = listing
                
                # Calculate total price before saving
                check_in = form.cleaned_data['check_in']
                check_out = form.cleaned_data['check_out']
                num_nights = (check_out - check_in).days
                booking.total_price = num_nights * listing.price_per_night
                
                # Now save the booking (this will trigger validation)
                booking.save()
                
                messages.success(request, 'Booking created successfully! Waiting for host confirmation.')
                return redirect('booking_detail', pk=booking.pk)
                
            except ValidationError as e:
                # Display validation errors to user
                for error in e.messages:
                    messages.error(request, error)
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
    else:
        form = BookingForm(listing=listing)
    
    return render(request, 'bookings/booking_form.html', {
        'form': form,
        'listing': listing
    })

class BookingListView(LoginRequiredMixin, ListView):
    """View for listing user's bookings"""
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10
    
    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user).select_related('listing', 'listing__host').order_by('-created_at')

class BookingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """View for displaying booking details"""
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'
    
    def test_func(self):
        booking = self.get_object()
        return self.request.user == booking.guest or self.request.user == booking.listing.host

@login_required
def cancel_booking(request, pk):
    """View for cancelling a booking"""
    booking = get_object_or_404(Booking, pk=pk, guest=request.user)
    
    if booking.status in ['pending', 'confirmed'] and booking.is_upcoming:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully.')
    else:
        messages.error(request, 'This booking cannot be cancelled.')
    
    return redirect('booking_detail', pk=pk)

@login_required
def host_bookings(request):
    """View for hosts to see bookings for their listings"""
    bookings = Booking.objects.filter(
        listing__host=request.user
    ).select_related('guest', 'listing').order_by('-created_at')
    
    return render(request, 'bookings/host_bookings.html', {'bookings': bookings})

@login_required
def confirm_booking(request, pk):
    """View for hosts to confirm bookings"""
    booking = get_object_or_404(Booking, pk=pk, listing__host=request.user)
    
    if booking.status == 'pending':
        booking.status = 'confirmed'
        booking.save()
        messages.success(request, 'Booking confirmed successfully.')
    else:
        messages.error(request, 'This booking cannot be confirmed.')
    
    return redirect('booking_detail', pk=pk)