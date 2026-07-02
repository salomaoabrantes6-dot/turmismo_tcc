import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Belas_Projecto.settings')

application = get_wsgi_application()

# --- CÓDIGO DE CRIAÇÃO AUTOMÁTICA DO ADMIN ---
try:
    from global_models.models import Usuario
    
    username = 'admin'
    email = 'admin@email.com'
    senha = '1234'
    
    if not Usuario.objects.filter(username=username).exists():
        print("Criando superusuário no banco de produção...")
        Usuario.objects.create_superuser(username=username, email=email, password=senha)
        print("Superusuário criado com sucesso!")
except Exception as e:
    print(f"Aviso na criação do superusuário: {e}")
# ---------------------------------------------