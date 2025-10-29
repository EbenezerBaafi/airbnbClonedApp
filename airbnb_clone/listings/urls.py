from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListingListView.as_view(), name='listing_list'),
    path('<int:pk>/', views.ListingDetailView.as_view(), name='listing_detail'),
    path('create/', views.ListingCreateView.as_view(), name='listing_create'),
    path('<int:pk>/update/', views.ListingUpdateView.as_view(), name='listing_update'),
    path('<int:pk>/delete/', views.ListingDeleteView.as_view(), name='listing_delete'),
    path('<int:pk>/add-image/', views.add_listing_image, name='add_listing_image'),
]