from django import forms
from .models import User, UserProfile


class UserForm(forms.ModelForm):
    class Meta:
        password = forms.CharField(widget=forms.PasswordInput())
        confirm_password=forms.CharField(widget=forms.PasswordInput())

        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

