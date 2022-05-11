from .models import OrdersReview
from django import forms

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = OrdersReview
        fields = ('content', 'order', 'reviewer',)
        widgets = {'book': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}