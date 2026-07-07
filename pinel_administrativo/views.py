from django.contrib.auth.decorators import login_required,  user_passes_test

from django.shortcuts import render, redirect, get_object_or_404
from global_models.models import PontoTuristico
from .forms import PontoTuristicoForm
from .forms import praiasForm
from global_models.models import praias
from django.contrib.auth.decorators import login_required
from global_models.models import Depoimento
from django.db.models import Count
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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from global_models.models import PontoTuristico, praias
from .forms import PontoTuristicoForm, praiasForm

# -----------------------------------------------------------------------------
# GESTÃO DE PONTOS TURÍSTICOS
# -----------------------------------------------------------------------------
@login_required
def pontos_turisticos(request, pk=None):
    """
    CRUD em uma página: se pk é passado, editamos, senão criamos.
    Protegido contra Internal Server Error (500).
    """
    if pk:
        ponto = get_object_or_404(PontoTuristico, pk=pk)
        form = PontoTuristicoForm(request.POST or None, request.FILES or None, instance=ponto)
    else:
        form = PontoTuristicoForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Ponto turístico guardado com sucesso!')
                return redirect('pontos_turisticos')
            except Exception as e:
                # Captura erros de banco de dados (ex: integridade, colunas nulas, caminhos de arquivo)
                messages.error(request, f'Erro interno ao gravar no banco de dados: {e}')
        else:
            # Captura falhas de preenchimento nos inputs do formulário
            messages.error(request, f'Erro de validação no formulário: {form.errors}')

    pontos = PontoTuristico.objects.all()
    return render(request, 'painel_administrativo/pontos_turisticos.html', {
        'form': form, 
        'pontos': pontos, 
        'pk': pk
    })


@login_required
def deletar_ponto(request, pk):
    """
    Remove um ponto turístico com captura de segurança.
    """
    ponto = get_object_or_404(PontoTuristico, pk=pk)
    if request.method == 'POST':
        try:
            ponto.delete()
            messages.success(request, 'Ponto turístico eliminado com sucesso.')
        except Exception as e:
            messages.error(request, f'Não foi possível eliminar o ponto turístico: {e}')
    return redirect('pontos_turisticos')


# -----------------------------------------------------------------------------
# GESTÃO DE PRAIAS
# -----------------------------------------------------------------------------
@login_required
def praiasBelas(request, pk=None):
    """
    CRUD de praias em uma única página.
    Protegido contra falhas críticas de salvamento.
    """
    if pk:
        praia = get_object_or_404(praias, pk=pk)
        form = praiasForm(request.POST or None, request.FILES or None, instance=praia)
    else:
        form = praiasForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Dados da praia guardados com sucesso!')
                return redirect('praias')
            except Exception as e:
                messages.error(request, f'Erro interno ao gravar a praia no banco: {e}')
        else:
            messages.error(request, f'Erro de validação no formulário da praia: {form.errors}')

    praias_belas = praias.objects.all()
    praias_belas_total = praias.objects.count()
    
    return render(request, 'painel_administrativo/praias.html', {
        'form': form,
        'praias_belas': praias_belas,
        'pk': pk,
        'praias_belas_total': praias_belas_total
    })


@login_required
def deletar_praia(request, pk):
    """
    Remove uma praia com captura de segurança.
    """
    deletPraia = get_object_or_404(praias, pk=pk)
    if request.method == 'POST':
        try:
            deletPraia.delete()
            messages.success(request, 'Praia eliminada com sucesso.')
        except Exception as e:
            messages.error(request, f'Não foi possível eliminar a praia: {e}')
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





