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
    
    return render(request, 'index.html', {'pontos': pontos, 'praias_belas': praias_belas, 'depoimentos': depoimentos }) 

    

def ladingPage(request):
    return render(request, 'ladingPage.html')
    

def login_view(request):
    if request.method == 'POST': 
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user_obj = get_user_model().objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except get_user_model().DoesNotExist:
            user = None
            
        if user is not None and user.is_superuser:
            auth_login(request, user)
            return redirect('/admin/')
        else:
            messages.error(request, 'Acesso negado: Apenas admin')
    
    return render(request, 'login.html')


def logout_view(request):
    auth_logout(request)
    return redirect('login')



    
         