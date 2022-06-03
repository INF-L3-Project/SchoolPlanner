from enum import Flag
from pprint import pprint
from authentication.models import Institution
from django.contrib.auth.models import User
from django import forms


class RegisterForm(forms.Form):
    last_name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    name = forms.CharField(max_length=255, required=True)
    logo = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        fields = ('last_name', 'email', 'password', 'name', 'logo',
                  'description')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Un compte avec cette adresse mail existe déjà")
        return email

    def save(self, commit=True):
        last_name = self.cleaned_data['last_name']
        username = self.cleaned_data['email']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username=username,
                                        last_name=last_name,
                                        email=email,
                                        password=password)

        return Institution.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            logo=self.cleaned_data['logo'],
            description=self.cleaned_data['description'])


class LoginForm(forms.Form):
    username = forms.EmailField()
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    class Meta:
        fields = ("username", "password")
