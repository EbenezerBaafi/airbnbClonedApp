from django.urls import path
from . import views

urlpatterns = [
    path('booking/<int:booking_pk>/create/', views.create_review, name='create_review'),
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
    path('<int:pk>/respond/', views.add_host_response, name='add_host_response'),
    path('listing/<int:listing_pk>/', views.ListingReviewsView.as_view(), name='listing_reviews'),
]