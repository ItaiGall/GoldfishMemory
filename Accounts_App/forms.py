from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from GoldfishMemory_App.models import Vehicle
import datetime

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'username',
            'id': 'username',
            'type': 'text',
            'placeholder':'Your Username',
            'maxlength': '16',
            'minlength': '6',
            })
        self.fields['username'].label = "Username"
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'email',
            'id': 'email',
            'type': 'email',
            'placeholder':'Your Email',
            })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'password1',
            'id': 'password1',
            'type': 'password',
            'placeholder': 'Your Password',
            'maxlength': '22',
            'minlength': '8',
            })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'password2',
            'id': 'password2',
            'type': 'password',
            'placeholder': 'Password Confirmation',
            'maxlength': '22',
            'minlength': '8',
            })

    username = forms.CharField(max_length=20, label=False)
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class RegisterVehicleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['license_number'].widget.attrs.update({
            'class': 'form-input',
            'required': 'True',
            'name': 'license_number',
            'id': 'license_number',
            'type': 'text',
            'placeholder':'License Number or car identification of your choice',
            'maxlength': '30',
            'minlength': '2',
            })
        self.fields['cookies_consent'].required = True
        self.fields['cookies_consent'].help_text = 'By accepting you agree to "Goldfish Memory\'s" cookie policy for security tokens and session state'
        self.fields['cookies_consent'].attrs = {'id': 'consent'}
    class Meta:
        model = Vehicle
        fields = ['license_number', 'cookies_consent']
        label = {'license_number':'License Number or car identification of your choice'}

class ChangeUserInfoForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Username"
    password = None
    username = forms.CharField(max_length=20, label=False)
    email = forms.EmailField(max_length=100)



