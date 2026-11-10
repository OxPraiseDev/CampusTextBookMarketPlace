from django import forms
from .models import Listing, Book

class CreateListingForm(forms.Form):
    # Book Details
    title = forms.CharField(max_length=200, label="Book Title")
    author = forms.CharField(max_length=150)
    isbn = forms.CharField(max_length=20, label="ISBN Number")
    edition = forms.CharField(max_length=50, label="Edition (e.g., 3rd)")
    subject = forms.CharField(max_length=100, label="Subject (e.g., CSC 101)")
    
    # Listing Details
    listing_type = forms.ChoiceField(choices=Listing.LISTING_TYPES)
    asking_price = forms.DecimalField(required=False, help_text="Leave blank if trading")
    condition = forms.ChoiceField(choices=Listing.CONDITIONS)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))