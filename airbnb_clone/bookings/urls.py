from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookingListView.as_view(), name='booking_list'),
    path('<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('listing/<int:listing_pk>/create/', views.create_booking, name='create_booking'),
    path('<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('<int:pk>/confirm/', views.confirm_booking, name='confirm_booking'),
    path('host/', views.host_bookings, name='host_bookings'),
]