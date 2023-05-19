from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from . models import *

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ('review_text', 'rating')

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('address', 'mobile', 'status')

class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')