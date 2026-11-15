from django import forms
from .models import Contact
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control border-0',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control border-0',
                'placeholder': 'Your Email'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control border-0',
                'placeholder': 'Subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control border-0',
                'placeholder': 'Message',
                'style': 'height:160px'
            }),
        }

class RegisterForm(forms.ModelForm):
    name = forms.CharField(max_length=150, required=True, label="Full Name")
    email = forms.EmailField(required=True, label="Email Address")
    mobile = forms.CharField(max_length=15, required=True, label="Mobile Number")
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=True, label="Address")
    image = forms.ImageField(required=False, label="Profile Image")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
    cpassword = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirm Password")

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'cpassword']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        cpassword = cleaned_data.get("cpassword")
        if password and cpassword and password != cpassword:
            self.add_error('cpassword', "Passwords do not match")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile', 'address', 'image']
        widgets = {
            'mobile': forms.TextInput(attrs={'placeholder': 'Enter your mobile number'}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter your address', 'rows': 3}),
        }