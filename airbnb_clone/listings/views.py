from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Avg
from .models import Listing, ListingImage
from .forms import ListingForm, ListingImageForm, ListingSearchForm

class ListingListView(ListView):
    """View for listing all properties"""
    model = Listing
    template_name = 'listings/listing_list.html'
    context_object_name = 'listings'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Listing.objects.filter(is_active=True).prefetch_related('images', 'reviews')
        
        # Search functionality
        location = self.request.GET.get('location')
        guests = self.request.GET.get('guests')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        bedrooms = self.request.GET.get('bedrooms')
        bathrooms = self.request.GET.get('bathrooms')
        property_type = self.request.GET.get('property_type')
        
        if location:
            queryset = queryset.filter(
                Q(city__icontains=location) | 
                Q(state__icontains=location) | 
                Q(country__icontains=location) |
                Q(title__icontains=location)
            )
        
        if guests:
            queryset = queryset.filter(guests__gte=guests)
        
        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)
        
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)
            
        if bedrooms:
            queryset = queryset.filter(bedrooms__gte=bedrooms)
            
        if bathrooms:
            queryset = queryset.filter(bathrooms__gte=bathrooms)
            
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ListingSearchForm(self.request.GET)
        return context

class ListingDetailView(DetailView):
    """View for displaying a single listing"""
    model = Listing
    template_name = 'listings/listing_detail.html'
    context_object_name = 'listing'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()
        context['reviews'] = self.object.reviews.select_related('reviewer').all()
        return context

class ListingCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new listing"""
    model = Listing
    form_class = ListingForm
    template_name = 'listings/listing_form.html'
    
    def form_valid(self, form):
        form.instance.host = self.request.user
        messages.success(self.request, 'Listing created successfully!')
        return super().form_valid(form)

class ListingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating an existing listing"""
    model = Listing
    form_class = ListingForm
    template_name = 'listings/listing_form.html'
    
    def test_func(self):
        listing = self.get_object()
        return self.request.user == listing.host
    
    def form_valid(self, form):
        messages.success(self.request, 'Listing updated successfully!')
        return super().form_valid(form)

class ListingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting a listing"""
    model = Listing
    template_name = 'listings/listing_delete.html'
    success_url = reverse_lazy('listing_list')
    
    def test_func(self):
        listing = self.get_object()
        return self.request.user == listing.host
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Listing deleted successfully!')
        return super().delete(request, *args, **kwargs)

@login_required
def add_listing_image(request, pk):
    """View for adding images to a listing"""
    listing = get_object_or_404(Listing, pk=pk, host=request.user)
    
    if request.method == 'POST':
        form = ListingImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.listing = listing
            image.save()
            messages.success(request, 'Image uploaded successfully!')
            return redirect('listing_detail', pk=pk)
    else:
        form = ListingImageForm()
    
    return render(request, 'listings/add_image.html', {'form': form, 'listing': listing})