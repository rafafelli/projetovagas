from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

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

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório para criar um usuário.")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255, default='')
    is_empresa = models.BooleanField(default=False)
    is_candidato = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Empresa(CustomUser):
    class Meta:
        proxy = True

class Candidato(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="candidato_profile")
    pretensao_salarial = models.CharField(max_length=20, choices=FAIXA_SALARIAL_CHOICES)
    escolaridade = models.CharField(max_length=50, choices=ESCOLARIDADE_CHOICES, null=True)

class Vaga(models.Model):
    nome = models.CharField(max_length=255)
    faixa_salarial = models.CharField(max_length=20, choices=FAIXA_SALARIAL_CHOICES)
    requisitos = models.TextField()
    escolaridade_minima = models.CharField(max_length=50, choices=ESCOLARIDADE_CHOICES)
    empresa = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vagas_empresa', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def aplicado(self, user):
        return self.aplicacoes.filter(candidato=user).exists()

    def __str__(self):
        return self.nome
    
class Aplicacao(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    candidato = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    data_aplicacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('vaga', 'candidato')

    def __str__(self):
        return f'{self.candidato.nome} aplicou para {self.vaga.nome}'
