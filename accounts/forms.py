from django import forms
from .models import Account, UserProfile
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r"^\+?\d{10,15}$",
    message="Enter a valid phone number (10–15 digits). You can start with +."
)

# At least 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char
password_validator = RegexValidator(
    regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$",
    message="Password must be 8+ chars and include upper, lower, number, and special character."
)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(validators=[password_validator],
                               widget=forms.PasswordInput
                               (attrs={'class': 'form-control', 'placeholder': 'Enter password'}))

    confirm_password = forms.CharField(widget=forms.PasswordInput
                                       (attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name',
                  'email', 'phone_number', 'password']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
        }
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and Account.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_phone_number(self):
        phone = (self.cleaned_data.get("phone_number") or "").strip()
        phone = phone.replace(" ", "").replace("-", "")
        phone_validator(phone)
        return phone

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get("password")
        cpwd = cleaned_data.get("confirm_password")
        if pwd and cpwd and pwd != cpwd:
            self.add_error("confirm_password", "Passwords do not match")



class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name','last_name','phone_number')


    def __init__(self,*args,**kwargs):
        super(UserForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False,
        error_messages={'invalid': "Image files only"},
        widget=forms.FileInput
    )
    class Meta:
        model = UserProfile
        fields = ('address_line1','address_line2','city','state','country','profile_picture')

    def __init__(self,*args,**kwargs):
        super(UserProfileForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'