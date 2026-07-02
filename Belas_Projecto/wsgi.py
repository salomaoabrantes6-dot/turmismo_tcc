import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Belas_Projecto.settings')

application = get_wsgi_application()

# --- FORÇAR SUPERUSUÁRIO NO BANCO POSTGRES ---
try:
    from global_models.models import Usuario
    
    email_admin = 'admin@email.com'
    senha_admin = '123456'
    
    # 1. Se não existir, cria. Se existir, não faz nada aqui.
    user, created = Usuario.objects.get_or_create(email=email_admin)
    
    # 2. Forçamos a nova senha por segurança
    user.set_password(senha_admin)
    user.save()
    
    # 3. O SEGREDO: Força a atualização direta das permissões no banco de dados
    Usuario.objects.filter(email=email_admin).update(
        is_superuser=True,
        is_staff=True,
        is_active=True
    )
    
    print("Sucesso: Permissões de Superusuário injetadas diretamente!")
except Exception as e:
    print(f"Aviso na configuração do admin: {e}")
# ---------------------------------------------