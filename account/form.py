from django import forms
from django.forms import ValidationError

from .models import User

class CustomUserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(max_length=255,)
    name = forms.CharField(max_length=255,)
    password = forms.CharField(max_length=16, min_length=8, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=16, min_length=8, widget=forms.PasswordInput)
    profile_image = forms.ImageField(max_length=255)
    tc = forms.BooleanField()

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise ValidationError("Passwords didn't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
    class Meta:
        model = User
        fields = ['email', 'name', 'tc', 'profile_image']