from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserBasicInfoForm(UserCreationForm):
    """Formulario para el paso 1: información básica del usuario"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        
class PersonalInfoForm(forms.ModelForm):
    """Formulario para el paso 2: información personal"""
    phone_number = forms.CharField(max_length=15, required=True)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'date_of_birth')
        
class AddressInfoForm(forms.ModelForm):
    """Formulario para el paso 3: información de dirección"""
    
    class Meta:
        model = UserProfile
        fields = ('address', 'city', 'state', 'postal_code')
        
class AdditionalInfoForm(forms.ModelForm):
    """Formulario para el paso 4: información adicional"""
    
    class Meta:
        model = UserProfile
        fields = ('bio',)