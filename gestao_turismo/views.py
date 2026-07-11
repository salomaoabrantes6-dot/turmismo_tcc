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

def is_superuser_or_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_superuser_or_admin, login_url='/gestao_turismo/login/')

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
    
    return render(request, 'gestao_turismo/dashboard.html', {
        'depoimentos': depoimentos,
        'total_depoimentos': total_depoimentos,
        'total_ponto': total_ponto,
        'pontos': pontos,
        'praias_belas': praias_belas,
        'total_imagens': total_imagens,
    })    

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
    return render(request, 'gestao_turismo/pontos_turisticos.html', {
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
    
    return render(request, 'gestao_turismo/praias.html', {
        'form': form,
        'praias_belas': praias_belas,
        'pk': pk,
        'praias_belas_total': praias_belas_total,
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

from django.shortcuts import render, redirect
from django.contrib import messages






