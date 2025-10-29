from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    """Form for creating reviews"""
    class Meta:
        model = Review
        fields = ['rating', 'cleanliness', 'communication', 'check_in', 
                  'accuracy', 'location', 'value', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5'}),
            'cleanliness': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5'}),
            'communication': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5'}),
            'check_in': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5'}),
            'accuracy': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5'}),
            'location': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class HostResponseForm(forms.ModelForm):
    """Form for host responses to reviews"""
    class Meta:
        model = Review
        fields = ['host_response']
        widgets = {
            'host_response': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }