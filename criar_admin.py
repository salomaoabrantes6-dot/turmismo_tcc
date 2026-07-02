import os
import django

# Diz ao script para usar as configurações do seu projeto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Belas_Projecto.settings')
django.setup()

# Importa o seu modelo de usuário personalizado
from global_models.models import Usuario 

username = 'admin'
email = 'admin@email.com'
senha = '1234'

if not Usuario.objects.filter(username=username).exists():
    print("Criando superusuário de produção...")
    Usuario.objects.create_superuser(username=username, email=email, password=senha)
    print("Superusuário criado com sucesso!")
else:
    print("O superusuário já existe no banco de dados do Render.")