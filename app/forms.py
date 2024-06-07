from django import forms
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm, PasswordResetForm


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter password', "type":"password"}))


class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'autocomplete': 'off'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'autocomplete': 'off'}))
    password1 = forms.CharField(label='Password', widget=forms.TextInput(attrs={'placeholder': 'Enter password', 'autocomplete': 'off'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.TextInput(attrs={'placeholder': 'Confirm Password', "type":"password"}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerProfileForm(forms.ModelForm):
    mobile = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Phone number', 'autocomplete': 'off'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Address name', 'autocomplete': 'off'}))
    locality = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Locality', 'autocomplete': 'off'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'State'}))
    zipcode = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Pin-Code','autocomplete': 'off'}))
    
    class Meta:
        model = Customer
        fields=['mobile', 'name', 'locality', 'city', 'state', 'zipcode']

# Password Update from profile page
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter old password', "type":"password"}))
    new_password1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter new password', 'autocomplete': 'off'}))
    new_password2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Confirm new password', "type":"password"}))


# Forgot password
class MyPasswordResetFrom(PasswordResetForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Your registered Email', 'autocomplete': 'off'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.TextInput(attrs={'placeholder': 'Enter New password', 'autocomplete': 'off'}))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.TextInput(attrs={'placeholder': 'Confirm new password', 'type': 'password'}))