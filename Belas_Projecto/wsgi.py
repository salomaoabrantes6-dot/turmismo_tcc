import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Belas_Projecto.settings')

application = get_wsgi_application()

# --- ABORDAGEM DIRETA PARA CRIAÇÃO DO ADMIN ---
try:
    from global_models.models import Usuario
    
    username_admin = 'admin'
    email_admin = 'admin@email.com'
    senha_admin = '0101'  # <--- Escolha a sua senha aqui
    
    if not Usuario.objects.filter(username=username_admin).exists():
        print("Criando superusuário de forma direta no banco...")
        
        # Cria a instância do usuário vazia e preenche os atributos manualmente
        user = Usuario()
        user.username = username_admin
        user.email = email_admin
        user.set_password(senha_admin)  # Criptografa a senha com segurança
        
        # Dá os poderes de administrador do Django
        user.is_superuser = True
        user.is_staff = True
        
        # Salva no banco de dados do Render
        user.save()
        
        print("Superusuário criado com sucesso!")
except Exception as e:
    print(f"Aviso na criação do superusuário: {e}")
# ---------------------------------------------