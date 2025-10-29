from django import forms
from .models import Listing, ListingImage

class ListingForm(forms.ModelForm):
    """Form for creating and updating listings"""
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'property_type',
            'street_address', 'city', 'state', 'country', 'zip_code',
            'bedrooms', 'bathrooms', 'guests', 'price_per_night',
            'wifi', 'kitchen', 'parking', 'air_conditioning', 
            'heating', 'tv', 'pool', 'gym', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

class ListingImageForm(forms.ModelForm):
    """Form for uploading listing images"""
    class Meta:
        model = ListingImage
        fields = ['image', 'caption', 'is_primary']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ListingSearchForm(forms.Form):
    """Form for searching listings"""
    location = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Where are you going?'}
    ))
    check_in = forms.DateField(required=False, widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date'}
    ))
    check_out = forms.DateField(required=False, widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date'}
    ))
    guests = forms.IntegerField(required=False, min_value=1, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Guests'}
    ))
    min_price = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Min Price'}
    ))
    max_price = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Max Price'}
    ))