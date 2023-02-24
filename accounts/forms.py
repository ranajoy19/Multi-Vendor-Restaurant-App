from django import forms
from .models import User, UserProfile

from django.forms import CharField, Form, PasswordInput

class UserForm(forms.ModelForm):
    confirm_password=forms.CharField(widget=forms.PasswordInput(),required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            # telling Django your password field in the mode is a password input on the template
            'password': forms.PasswordInput() ,
            'confirm_password': forms.PasswordInput() 
        }
        
    def clean(self):
        cleaned_data = super(UserForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )