import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Belas_Projecto.settings')

application = get_wsgi_application()

# --- INSTALAÇÃO FORÇADA DO ADMINISTRADOR ---
try:
    from global_models.models import Usuario
    
    username_admin = 'admin'
    email_admin = 'admin@email.com'
    senha_admin = '123456'  # <--- Certifique-se de usar esta sem espaços
    
    # Buscamos se já existe, ou criamos um do zero
    user, created = Usuario.objects.get_or_create(username=username_admin)
    
    if created:
        print("Criando utilizador admin do zero...")
        user.email = email_admin
    else:
        print("Utilizador já existia. Forçando atualização de permissões...")

    # Forçamos todas as flags de segurança do Django
    user.set_password(senha_admin)
    user.is_superuser = True
    user.is_staff = True
    user.is_active = True  # <--- MUITO IMPORTANTE: Garante que a conta não está bloqueada
    user.save()
    
    print("Administrador atualizado e ativo com sucesso!")
except Exception as e:
    print(f"Aviso na criação do superusuário: {e}")
# ---------------------------------------------