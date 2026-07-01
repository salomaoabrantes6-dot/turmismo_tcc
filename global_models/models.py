from django.db import models
# Create your models here.
class PontoTuristico(models.Model):
    imagem_ponto = models.ImageField(
        upload_to='fotos_dos_pontos/',
        verbose_name="Imagem principal",
        help_text="Foto destaque do ponto turístico"
    )

    imagem_1 = models.ImageField(
        upload_to='fotos_dos_pontos/',
        verbose_name="Imagem ilustrativa 1",
        help_text="Primeira imagem complementar (ex: vista geral)"
    )
    imagem_2 = models.ImageField(
        upload_to='fotos_dos_pontos/',
        verbose_name="Imagem ilustrativa 2",
        help_text="Segunda imagem complementar (ex: detalhe arquitetônico)"
    )
    imagem_3 = models.ImageField(
        upload_to='fotos_dos_pontos/',
        verbose_name="Imagem ilustrativa 3",
        help_text="Terceira imagem complementar (ex: interior ou evento)"
    )
    imagem_4 = models.ImageField(
        upload_to='fotos_dos_pontos/',
        verbose_name="Imagem ilustrativa 4",
        help_text="Quarta imagem complementar (ex: entorno ou acesso)"
    )
    
    titulo_ponto = models.CharField(
        max_length=200,
        verbose_name="Título do ponto turístico"
    )
    descricao_ponto = models.TextField(
        verbose_name="Descrição detalhada"
    )
    localizacao_ponto = models.CharField(
        max_length=300,
        verbose_name="Localização (cidade, bairro, endereço completo)"
    )
    servicos_prestados_ponto = models.TextField(
        verbose_name="Serviços oferecidos (guia, estacionamento, acessibilidade, etc.)"
    )
    horario_atendimento_ponto = models.CharField(
        max_length=200,
        verbose_name="Horário de funcionamento"
    )
    contacto_ponto = models.CharField(
        max_length=150,
        verbose_name="Contato (telefone, WhatsApp, e-mail)"
    )

    imagem_hotel = models.ImageField(
        upload_to='fotos_dos_hoteeis/',
        verbose_name="Imagem principal",
        help_text="Foto destaque do hotel"
    )

    titulo_hotel = models.CharField(
        max_length=200,
        verbose_name="Nome do hotel"
    )
    descricao_hotel = models.TextField(
        verbose_name="Descrição detalhada do hotel"
    )
    localizacao_hotel = models.CharField(
        max_length=300,
        verbose_name="Localização (cidade, bairro, endereço completo)"
    )
    servicos_prestados_hotel = models.TextField(
        verbose_name="Serviços oferecidos (guia, estacionamento, psina, etc.)"
    )
    horario_hotel = models.CharField(
        max_length=200,
        verbose_name="Horário de funcionamento"
    )
    contacto_hotel = models.CharField(
        max_length=150,
        verbose_name="Contato (telefone, WhatsApp, e-mail)"
    )
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name = "Ponto Turístico"
        verbose_name_plural = "Pontos Turísticos"
        ordering = ['-data_criacao']

    def __str__(self):
        return f"PontoTuristico {self.id}"


class praias(models.Model):
        imagem_praia = models.ImageField(
        upload_to='fotos_das_praias/',
        verbose_name="Imagem principal",
    )
        titulo_praia = models.CharField(
        max_length=200,
        verbose_name="Nome da práia",
    )
        descricao_praia = models.TextField(
        verbose_name="Descrição detalhada"
    )
        localizacao_ponto = models.CharField(
        max_length=300,
        verbose_name="Localização (cidade, bairro, endereço completo)"
    )
        

class Depoimento(models.Model):
    nome = models.CharField(max_length=100)
    mensagem = models.TextField()
    nota = models.IntegerField()
    image_url = models.URLField(blank=True, null=True)
    image_file = models.ImageField(upload_to='depoimentos/', blank=True, null=True)
    publicado = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.nota} estrelas"   



from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class UsuarioManager(BaseUserManager):
    """Gerenciador personalizado para o modelo Usuario"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('tipo', 'SUPER_ADMIN')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    """Modelo de usuário personalizado para o sistema"""
    
    class TipoUsuario(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
    
    # Campos personalizados
    email = models.EmailField('E-mail', unique=True, db_index=True)
    nome_completo = models.CharField('Nome completo', max_length=200)
    telefone = models.CharField('Telefone', max_length=20, blank=True, null=True)
    
    tipo = models.CharField(
        'Tipo de usuário',
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.ADMIN,
        help_text='Define se é Administrador ou Super Admin'
    )
    
    # Status personalizado (alternativa ao is_active)
    ativo = models.BooleanField('Ativo', default=True, help_text='Indica se o usuário está ativo no sistema')
    
    # Campos de auditoria
    data_criacao = models.DateTimeField('Data de criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Última atualização', auto_now=True)
    criado_por = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios_criados',
        verbose_name='Criado por'
    )
    
    # Campo para soft delete (opcional)
    excluido = models.BooleanField('Excluído', default=False, help_text='Soft delete - marca como excluído sem remover do banco')
    data_exclusao = models.DateTimeField('Data de exclusão', null=True, blank=True)
    
    # Configuração do manager
    objects = UsuarioManager()
    
    # Campos obrigatórios para autenticação
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo']
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['tipo']),
            models.Index(fields=['ativo']),
        ]
    
    def __str__(self):
        return f'{self.nome_completo} ({self.email})'
    
    def save(self, *args, **kwargs):
        # Sincroniza username com email
        if not self.username:
            self.username = self.email
        
        # Atualiza is_staff e is_superuser baseado no tipo
        if self.tipo == self.TipoUsuario.SUPER_ADMIN:
            self.is_staff = True
            self.is_superuser = True
        elif self.tipo == self.TipoUsuario.ADMIN:
            self.is_staff = True
            self.is_superuser = False
        
        # Sincroniza is_active com ativo
        self.is_active = self.ativo
        
        super().save(*args, **kwargs)
    
    @property
    def is_admin(self):
        """Retorna True se for Administrador ou Super Admin"""
        return self.tipo in [self.TipoUsuario.ADMIN, self.TipoUsuario.SUPER_ADMIN]
    
    def soft_delete(self, user=None):
        """Realiza soft delete do usuário"""
        self.excluido = True
        self.ativo = False
        self.is_active = False
        self.data_exclusao = timezone.now()
        self.save()
    
    def restore(self):
        """Restaura usuário excluído (soft delete)"""
        self.excluido = False
        self.ativo = True
        self.is_active = True
        self.data_exclusao = None
        self.save()
    
    def ativar(self):
        """Ativa o usuário"""
        self.ativo = True
        self.is_active = True
        self.save()
    
    def inativar(self):
        """Inativa o usuário"""
        self.ativo = False
        self.is_active = False
        self.save()


           
    