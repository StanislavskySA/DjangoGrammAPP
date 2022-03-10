from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm

from .models import User


class EditProfileForm(UserChangeForm):
    username = forms.CharField(label='Login',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'})
                               )
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control'})
                             )
    first_name = forms.CharField(label='First name',
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control'})
                                 )
    last_name = forms.CharField(label='Last name',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control'})
                                )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'})
                               )
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control'})
                             )
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'})
                                )
    password2 = forms.CharField(label='Password conf',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'})
                                )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'})
                               )
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control'})
                               )

    class Meta:
        model = User
        fields = ('username', 'password')
