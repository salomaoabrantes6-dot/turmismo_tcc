from django.contrib.auth.decorators import login_required,  user_passes_test

from django.shortcuts import render, redirect, get_object_or_404
from global_models.models import PontoTuristico
from .forms import PontoTuristicoForm
from .forms import praiasForm
from global_models.models import praias
from django.contrib.auth.decorators import login_required
from global_models.models import Depoimento
from django.db.models import Count
from bs4 import BeautifulSoup
# Create your views here.

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_superuser, login_url='/Aplicativo_Belas/login/')

def dashboard(request):
    depoimentos = Depoimento.objects.all()
    total_depoimentos = Depoimento.objects.count()
    pontos = PontoTuristico.objects.all()
    total_ponto = PontoTuristico.objects.count()
    praias_belas = praias.objects.all()
    
    # 🔹 Isso conta automaticamente todos os objetos que têm imagem
    # (ajuste "imagem" para o nome do seu campo)
    total_imagens = (
        depoimentos.exclude(image_file='').count() + 
        
        pontos.exclude(imagem_hotel='').count() + 
        pontos.exclude(imagem_1='').count() +
        pontos.exclude(imagem_2='').count() +
        pontos.exclude(imagem_3='').count() +
        pontos.exclude(imagem_4='').count() +
        pontos.exclude(imagem_ponto='').count() + 
        praias_belas.exclude(imagem_praia='').count()
    )
    
    return render(request, 'painel_administrativo/dashboard.html', {
        'depoimentos': depoimentos,
        'total_depoimentos': total_depoimentos,
        'total_ponto': total_ponto,
        'pontos': pontos,
        'praias_belas': praias_belas,
        'total_imagens': total_imagens,
    })    

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='admin:login')
def usuarios(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Lógica para criar novo admin
        if action == 'create':
            form = CriarAdminForm(request.POST)
            if form.is_valid():
                nome = form.cleaned_data['nome_completo']
                email = form.cleaned_data['email']
                telefone = form.cleaned_data.get('telefone', '')
                senha = form.cleaned_data['senha']
                tipo = form.cleaned_data['tipo']

                user = Usuario.objects.create_user(
                    email=email,
                    password=senha,
                    nome_completo=nome,
                    telefone=telefone,
                    tipo=tipo,
                    criado_por=request.user
                )
                
                tipo_display = dict(Usuario.TipoUsuario.choices).get(tipo)
                messages.success(request, f'{tipo_display} {email} criado com sucesso!')
                return redirect('usuarios')
            else:
                messages.error(request, 'Erro ao criar usuário. Verifique os dados.')
        
        # Lógica para gerenciar admins (ativar/desativar/excluir)
        elif action in ['toggle_active', 'delete']:
            user_id = request.POST.get('user_id')
            
            try:
                user = Usuario.objects.get(
                    pk=user_id, 
                    is_staff=True, 
                    excluido=False
                )
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
                return redirect('usuarios')

            # Impede auto-alteração
            if user == request.user and action in ['delete', 'toggle_active']:
                messages.error(request, 'Você não pode alterar seu próprio status.')
                return redirect('usuarios')

            if action == 'toggle_active':
                if user.ativo:
                    user.inativar()
                    messages.success(request, f'Usuário {user.email} foi inativado.')
                else:
                    user.ativar()
                    messages.success(request, f'Usuário {user.email} foi ativado.')

            elif action == 'delete':
                user.soft_delete(user=request.user)
                messages.success(request, f'Usuário {user.email} foi excluído.')

            return redirect('usuarios')
    
    # GET - Exibe a página
    else:
        form = CriarAdminForm()
        
        # Busca todos os admins (não excluídos)
        all_users = Usuario.objects.filter(
            is_staff=True, 
            excluido=False
        ).order_by('-data_criacao')
        
        contexto = {
            'form': form,
            'all_users': all_users,
            'tipos_usuario': dict(Usuario.TipoUsuario.choices),
        }
        
        return render(request, 'painel_administrativo/user.html', contexto)

    

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def logout_view(request):
    auth_logout(request)
    return redirect('index')


# appAdmin/views.py


@login_required
def pontos_turisticos(request, pk=None):
    """
    CRUD em uma página: se pk é passado, editamos, senão criamos
    """
    if pk:
        ponto = get_object_or_404(PontoTuristico, pk=pk)
        form = PontoTuristicoForm(request.POST or None, request.FILES or None, instance=ponto)
    else:
        form = PontoTuristicoForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('pontos_turisticos')  # volta para a mesma página

    pontos = PontoTuristico.objects.all()
    return render(request, 'painel_administrativo/pontos_turisticos.html', {'form': form, 'pontos': pontos, 'pk': pk})

# Adicionar praias
@login_required
def praiasBelas(request, pk=None):
    if pk:
        praia = get_object_or_404(praias, pk=pk)
        form = praiasForm(request.POST or None, request.FILES or None, instance=praia)
    else:
        form = praiasForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('praias')

    praias_belas = praias.objects.all()
    praias_belas_total = praias.objects.count()
    
    # Apenas depoimentos que ainda não foram publicados
    
    return render(request, 'painel_administrativo/praias.html', {
        'form': form,
        'praias_belas': praias_belas,
        'pk': pk,
        'praias_belas_total': praias_belas_total
    })



@login_required
def deletar_ponto(request, pk):
    ponto = get_object_or_404(PontoTuristico, pk=pk)
    if request.method == 'POST':
        ponto.delete()
    return redirect('pontos_turisticos')

@login_required
def deletar_praia(request, pk):
    deletPraia = get_object_or_404(praias, pk=pk)
    if request.method == 'POST':
        deletPraia.delete()
    return redirect('praias')
    
#Deletar depoimento

def acao_depoimento(request, id, acao):
    depoimento = get_object_or_404(Depoimento, id=id)
    if acao == 'postar':
        depoimento.publicado = True
        depoimento.save()
    elif acao == 'eliminar':
        depoimento.delete()
    
    return redirect('dashboard')

 
# Views de criacao de usuario
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from global_models.models import Usuario
from .forms import CriarAdminForm





