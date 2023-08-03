from django import forms
from .models import CustomUser, Candidato, Vaga

FAIXA_SALARIAL_CHOICES = (
    ('1', 'Até R$ 1.000,00'),
    ('2', 'De R$ 1.000,00 a R$ 2.000,00'),
    ('3', 'De R$ 2.000,00 a R$ 3.000,00'),
    ('4', 'Acima de R$ 3.000,00'),
)

ESCOLARIDADE_CHOICES = (
    ('1', 'Ensino Fundamental'),
    ('2', 'Ensino Médio'),
    ('3', 'Tecnólogo'),
    ('4', 'Ensino Superior'),
    ('5', 'Pós / MBA / Mestrado'),
    ('6', 'Doutorado'),
)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')
    
    class Meta:
        model = CustomUser
        fields = ['nome', 'email', 'password']

class EmpresaForm(UserForm):
    pass

class CandidatoForm(UserForm):
    pretensao_salarial = forms.ChoiceField(choices=FAIXA_SALARIAL_CHOICES)
    escolaridade = forms.ChoiceField(choices=ESCOLARIDADE_CHOICES)

    class Meta(UserForm.Meta):
        fields = UserForm.Meta.fields + ['pretensao_salarial', 'escolaridade']


class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['nome', 'faixa_salarial', 'requisitos', 'escolaridade_minima']
