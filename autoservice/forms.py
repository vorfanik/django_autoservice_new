from .models import OrdersReview, Profile, Order
from django import forms
from django.contrib.auth.models import User

class OrderReviewForm(forms.ModelForm):
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

class DateInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class UserOrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['car_id', 'return_time', 'status']
        widgets = {'return_time': DateInput()}