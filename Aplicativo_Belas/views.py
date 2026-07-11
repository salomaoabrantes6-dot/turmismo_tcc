from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth import get_user_model

# Create your views here.
# appPublico/views.py
from django.shortcuts import render
from global_models.models import PontoTuristico
from global_models.models import praias
from django.shortcuts import render, redirect, get_object_or_404
from global_models.models import Depoimento

def index(request):
    pontos = PontoTuristico.objects.all()
    praias_belas = praias.objects.all()
    depoimentos = Depoimento.objects.all()
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        mensagem = request.POST.get('descricao')
        nota = request.POST.get('avaliacao')
        url = request.POST.get('url')
        arquivo = request.FILES.get('imagem')

        # Criar o registro no banco de dados
        Depoimento.objects.create(
            nome=nome,
            mensagem=mensagem,
            nota=nota,
            image_url=url,
            image_file=arquivo
        )
        
       
        messages.success(request, 'Obrigado pelo seu depoimento!')
        return redirect('index')
    
    return render(request, 'index.html', {'pontos': pontos, 'praias_belas': praias_belas, 'depoimentos': depoimentos }) 

    

def ladingPage(request):
    return render(request, 'ladingPage.html')
    

def login_view(request):
    # Se já estiver logado, vai direto para o painel
        
    if request.method == 'POST': 
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # 🔹 CORRECÇÃO: O Django espera o identificador único (e-mail) no parâmetro 'username'
        user = authenticate(request, username=email, password=password)
            
        if user is not None:
            auth_login(request, user)
            if user.tipo == user.TipoUsuario.SUPER_ADMIN:
                return redirect('/admin/')  # Redireciona com sucesso para o painel administrativo
            
            elif user.tipo == user.TipoUsuario.ADMIN:
                return redirect('/admin/')
            else:
                messages.error(request, 'Acesso negado: Esta conta não tem permissões de Superusuário.')
        else:
            messages.error(request, 'E-mail ou palavra-passe incorretos.')
            
    return render(request, 'login.html')


def logout_view(request):
    auth_logout(request)
    return redirect('login')



    
         