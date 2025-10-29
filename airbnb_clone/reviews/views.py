from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Review
from .forms import ReviewForm, HostResponseForm
from bookings.models import Booking

@login_required
def create_review(request, booking_pk):
    """View for creating a review after a completed booking"""
    booking = get_object_or_404(Booking, pk=booking_pk, guest=request.user)
    
    # Check if booking is completed and review doesn't exist
    if booking.status != 'completed' or booking.check_out > timezone.now().date():
        messages.error(request, 'You can only review completed bookings.')
        return redirect('booking_detail', pk=booking_pk)
    
    if hasattr(booking, 'review'):
        messages.error(request, 'You have already reviewed this booking.')
        return redirect('booking_detail', pk=booking_pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.listing = booking.listing
            review.reviewer = request.user
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('listing_detail', pk=booking.listing.pk)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/review_form.html', {
        'form': form,
        'booking': booking
    })

class ReviewDetailView(DetailView):
    """View for displaying a single review"""
    model = Review
    template_name = 'reviews/review_detail.html'
    context_object_name = 'review'

@login_required
def add_host_response(request, pk):
    """View for hosts to respond to reviews"""
    review = get_object_or_404(Review, pk=pk, listing__host=request.user)
    
    if request.method == 'POST':
        form = HostResponseForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Response added successfully!')
            return redirect('review_detail', pk=pk)
    else:
        form = HostResponseForm(instance=review)
    
    return render(request, 'reviews/host_response_form.html', {
        'form': form,
        'review': review
    })

class ListingReviewsView(ListView):
    """View for displaying all reviews for a listing"""
    model = Review
    template_name = 'reviews/listing_reviews.html'
    context_object_name = 'reviews'
    paginate_by = 10
    
    def get_queryset(self):
        self.listing_pk = self.kwargs['listing_pk']
        return Review.objects.filter(listing__pk=self.listing_pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from listings.models import Listing
        context['listing'] = get_object_or_404(Listing, pk=self.listing_pk)
        return context