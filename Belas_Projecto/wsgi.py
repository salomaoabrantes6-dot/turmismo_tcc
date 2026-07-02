import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Belas_Projecto.settings')

application = get_wsgi_application()

# --- CÓDIGO DE CRIAÇÃO AUTOMÁTICA DO ADMIN (CORRIGIDO) ---
try:
    from global_models.models import Usuario
    
    username_admin = 'admin'
    email_admin = 'admin@email.com'
    senha_admin = '1234'  # <--- Escolhe a senha aqui
    
    if not Usuario.objects.filter(username=username_admin).exists():
        print("Criando superusuário no banco de produção...")
        # Corrigido: Passamos o username como o primeiro argumento posicional
        Usuario.objects.create_superuser(username_admin, email=email_admin, password=senha_admin)
        print("Superusuário criado com sucesso!")
except Exception as e:
    print(f"Aviso na criação do superusuário: {e}")
# ---------------------------------------------