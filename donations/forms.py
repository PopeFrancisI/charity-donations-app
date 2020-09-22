from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


def is_alpha_validator(value):
    for char in value:
        if not char.isalpha() and char not in r"'- ":
            raise ValidationError("Only letters allowed.")


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Imię'}),
        validators=(is_alpha_validator, )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
        validators=(is_alpha_validator, )
    )
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Hasło', 'type': 'password'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Powtórz hasło', 'type': 'password'}))

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )
