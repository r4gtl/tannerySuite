from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class FormRegistrazione(UserCreationForm):
    email = forms.CharField(max_length=30, required=True, widget=forms.EmailInput())
    
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
        
        


# Create a UserUpdateForm to update a username and email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

# Create a ProfileUpdateForm to update image.
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']