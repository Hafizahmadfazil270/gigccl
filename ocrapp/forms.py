from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'

        
class SignupForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields=['username','email']
        labels={'email':'Email'}


class EditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username','email']
        labels={'email':'Email'}