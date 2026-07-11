
# appAdmin/forms.py
from django import forms
from global_models.models import PontoTuristico
from global_models.models import praias

class PontoTuristicoForm(forms.ModelForm):
    class Meta:
        model = PontoTuristico
        fields = '__all__'
        
class praiasForm(forms.ModelForm):
    class Meta:
        model = praias
        fields = '__all__'

from django import forms
from django.core.exceptions import ValidationError
from global_models.models import Usuario

class CriarAdminForm(forms.Form):
    nome_completo = forms.CharField(
        max_length=200, 
        label='Nome completo',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        max_length=254, 
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    telefone = forms.CharField(
        max_length=20, 
        required=False, 
        label='Telefone',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label='Senha'
    )
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label='Confirmar senha'
    )
    tipo = forms.ChoiceField(
        choices=Usuario.TipoUsuario.choices,
        label='Tipo de administrador',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email, excluido=False).exists():
            raise ValidationError('Já existe um usuário com este e-mail.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar = cleaned_data.get('confirmar_senha')
        if senha and confirmar and senha != confirmar:
            raise ValidationError('As senhas não coincidem.')
        return cleaned_data

        
        