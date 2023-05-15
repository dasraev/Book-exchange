from django import forms
from .models import MyUser, Region
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['email', 'country', 'region', 'education', 'password1', 'password2']

    def clean_email(self):
        if MyUser.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(f"The {self.cleaned_data['email']} has already registerd")
        return self.cleaned_data['email']

    def clean_region(self, *args, **kwargs):
        if self.cleaned_data.get('region') not in Region.objects.filter(country=self.cleaned_data.get('country')):
            raise forms.ValidationError('This region isnt the part of selected country')
        return self.cleaned_data.get('region')


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )


class ProfileForm(UserChangeForm):
    email = forms.EmailField()

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'country', 'region', 'education', 'profile_pic', 'gender', 'age']

    def clean_region(self, *args, **kwargs):
        if self.cleaned_data.get('region') not in Region.objects.filter(country=self.cleaned_data.get('country')):
            raise forms.ValidationError('This region isnt the part of selected country')
        return self.cleaned_data.get('region')
