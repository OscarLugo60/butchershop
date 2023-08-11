from django import forms
from django.contrib.auth import authenticate
#
from .models import User

class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class': 'input-group-field',
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir Contraseña',
                'class': 'input-group-field',
            }
        )
    )

    class Meta:
        """Meta definition for Userform."""

        model = User
        fields = (
            'user',
            'full_name',
            'ocupation',
            'genero',
            'date_birth',
        )
        widgets = {
            'user': forms.TextInput(
                attrs={
                    'placeholder': 'Correo Electronico ...',
                    'class': 'input-group-field',
                }
            ),
            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre y apellido ...',
                    'class': 'input-group-field',
                }
            ),
            'ocupation': forms.Select(
                attrs={
                    'placeholder': 'Ocupacion ...',
                    'class': 'input-group-field',
                }
            ),
            'date_birth': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'input-group-field',
                },
            ),
        }
    
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son iguales')


class LoginForm(forms.Form):
    user = forms.CharField(
        label='Nombre de usuario',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'input-group-field',
                'placeholder': 'Nombre de usuario',
            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input-group-field',
                'placeholder': 'contraseña'
            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        user = self.cleaned_data['user']
        password = self.cleaned_data['password']

        if not authenticate(user=user, password=password):
            raise forms.ValidationError('Los datos de usuario no son correctos')
        
        return self.cleaned_data


class UserUpdateForm(forms.ModelForm):

    class Meta:

        model = User
        fields = (
            'user',
            'full_name',
            'ocupation',
            'genero',
            'date_birth',
            'is_active',
        )
        widgets = {
            'user': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre de usuario ...',
                    'class': 'input-group-field',
                }
            ),
            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre y apellido ...',
                    'class': 'input-group-field',
                }
            ),
            'ocupation': forms.Select(
                attrs={
                    'placeholder': 'Ocupacion ...',
                    'class': 'input-group-field',
                }
            ),
            'date_birth': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'input-group-field',
                },
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                },
            ),
        }


class UpdatePasswordForm(forms.Form):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Actual'
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Nueva'
            }
        )
    )