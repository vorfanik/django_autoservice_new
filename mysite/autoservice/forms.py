from .models import OrdersReview
from django import forms
from .models import Profile
from django.contrib.auth.models import User

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = OrdersReview
        fields = ('content', 'order', 'reviewer',)
        widgets = {'book': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']