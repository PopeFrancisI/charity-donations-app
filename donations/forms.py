from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, MinLengthValidator
from django.forms import ModelForm


def is_alpha_validator(value):
    for char in value:
        if not char.isalpha() and char not in r"'- ":
            raise ValidationError("Dozwolone są tylko litery.")


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


class UserProfileEditForm(ModelForm):

    username = forms.EmailField(validators=(validate_email, ), label="Email")
    first_name = forms.CharField(min_length=2, max_length=150, label="Imię")
    last_name = forms.CharField(min_length=2, max_length=150, label="Nazwisko")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
