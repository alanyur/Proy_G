from django import forms
from .models import Solicitud

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'User name / Email',
        'class': 'sesion_input'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'sesion_input'
    }))

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe tu solicitud'}),
        }
