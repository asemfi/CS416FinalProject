from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


# Rana Naimat
class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ("username", 'first_name', "last_name", 'email', 'password1', 'password2')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", 'first_name', "last_name", 'email')


class EditUserForm(UserForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta(UserForm.Meta):
        fields = ("username", 'first_name', "last_name", 'email')
