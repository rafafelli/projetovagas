from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count
from .forms import  CandidatoForm, EmpresaForm, UserForm, VagaForm
from django.db.models.functions import ExtractMonth
from .models import Vaga, Aplicacao, Candidato

@login_required
def vagas_aplicadas(request):
    aplicacoes = Aplicacao.objects.filter(candidato=request.user)
    vagas_aplicadas = [aplicacao.vaga for aplicacao in aplicacoes]

    for vaga in vagas_aplicadas:
        vaga.aplicado = True
        vaga.total_aplicados = vaga.aplicacao_set.count()
        vaga.candidatos = [aplicacao.candidato for aplicacao in vaga.aplicacao_set.all()]

    return render(request, 'vagas/ver_vagas_aplicadas.html', {'vagas': vagas_aplicadas})

        
@login_required
def cancelar_aplicacao(request, vaga_id):

    is_aplicada = request.GET.get('aplicadas')

    vaga = get_object_or_404(Vaga, id=vaga_id)
    aplicacao = get_object_or_404(Aplicacao, vaga=vaga, candidato=request.user)

    aplicacao.delete()

    messages.success(request, 'Você cancelou sua aplicação para esta vaga.')

    if is_aplicada:
        return HttpResponseRedirect(reverse('empregos:vagas_aplicadas'))
    else:
        return HttpResponseRedirect(reverse('empregos:ver_vagas'))

@login_required
def aplicar_vaga(request, vaga_id):

    vaga = get_object_or_404(Vaga, id=vaga_id)

    Aplicacao.objects.create(vaga=vaga, candidato=request.user)

    messages.success(request, 'Parabéns, agora você está aplicado nesta vaga.')
    
    return HttpResponseRedirect(reverse('empregos:ver_vagas'))

@login_required
def vagas_view(request):
    if request.user.is_authenticated:
        if request.user.is_candidato:
            return render(request, 'empregos/candidato_vagas.html')

        elif request.user.is_empresa:
            return render(request, 'empregos/empresa_vagas.html')

    else:
        return redirect('empregos:login')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('empregos:home')
        else:
            error_message = "Credenciais inválidas. Por favor, tente novamente."
            return render(request, 'registration/login.html', {'error_message': error_message})
    else:
        return render(request, 'registration/login.html')

def registro_view(request):
    tipo_cadastro = request.POST.get('tipo_cadastro') if request.method == 'POST' else 'candidato'
    form = CandidatoForm(request.POST) if tipo_cadastro == 'candidato' else EmpresaForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])

        if tipo_cadastro == 'candidato':
            user.is_candidato = True
            user.save()
            candidato = Candidato(
                user=user,
                pretensao_salarial=form.cleaned_data['pretensao_salarial'],
                escolaridade=form.cleaned_data['escolaridade']
            )
            candidato.save()
        else:
            user.is_empresa = True
            user.save()

        login(request, user)
        return redirect('empregos:home')

    return render(request, 'registration/registro.html', {'form': form})

def home(request):
    user = request.user
    return render(request, 'empregos/home.html', {'user': user})

def logout_view(request):
    logout(request)
    return redirect('empregos:home')
    
def criar_vaga(request):
    if request.method == 'POST':
        form = VagaForm(request.POST)
        if form.is_valid():
            vaga = form.save(commit=False)  
            vaga.empresa = request.user  
            vaga.save()  
            messages.success(request, 'A Vaga Foi Criada com Sucesso!')
            return redirect('empregos:vagas')
    else:
        form = VagaForm()

    return render(request, 'vagas/form_vaga.html', {'form': form})

def ver_vagas(request):

    vagas = filtrar_vagas(request)

    return render(request, 'vagas/ver_vaga.html', {'vagas': vagas})

@csrf_exempt
def deletar_vaga(request, vaga_id):
    if not request.user.is_authenticated:
        return redirect('contas:login')
    if not request.user.is_empresa:
        return redirect('empregos:candidato_vagas')

    vaga = get_object_or_404(Vaga, id=vaga_id, empresa=request.user)
    vaga.delete()
    messages.success(request, 'A Vaga Foi Excluída com Sucesso!')
    
    return redirect('empregos:ver_vagas')
    
def editar_vaga(request, vaga_id):
    
    vaga = Vaga.objects.get(id=vaga_id)

    if request.method == 'POST':
        form = VagaForm(request.POST, instance=vaga)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vaga Editada Com Sucesso!')
            return redirect('empregos:ver_vagas')
    else:
        form = VagaForm(instance=vaga)

    return render(request, 'vagas/form_vaga.html', {'form': form, 'vaga': vaga})

def filtrar_vagas(request):

    pretensao_salarial = request.POST.getlist('pretensaoSalarial')
    escolaridade_minima = request.POST.getlist('escolaridadeMinima')
    user = request.user

    if user.is_empresa:
        vagas = Vaga.objects.filter(empresa=user)
    else:
        vagas = Vaga.objects.all()

    if request.method == 'POST':
        if pretensao_salarial != ['']:
            vagas = vagas.filter(faixa_salarial__in=pretensao_salarial)

        if escolaridade_minima != ['']:
            vagas = vagas.filter(escolaridade_minima__in=escolaridade_minima)

        if len(vagas) == 0:
            messages.success(request, 'Nenhuma vaga Encontrada')

    for vaga in vagas:
        vaga.aplicado = vaga.aplicacao_set.filter(candidato=request.user).exists()
        aplicacoes = vaga.aplicacao_set.all()
        vaga.total_aplicados = aplicacoes.count()
        vaga.candidatos = [aplicacao.candidato for aplicacao in aplicacoes]

        if user.is_empresa:
            candidatos_com_pontuacao = []
            for aplicacao in aplicacoes:
                candidato = aplicacao.candidato
                candidato.pontuacao = 0
                
                if int(candidato.candidato_profile.pretensao_salarial) == int(vaga.faixa_salarial):
                    candidato.pontuacao += 1
                
                if int(candidato.candidato_profile.escolaridade) >= int(vaga.escolaridade_minima):
                    candidato.pontuacao += 1

                candidatos_com_pontuacao.append(candidato)

            vaga.candidatos = candidatos_com_pontuacao
        else:
            vaga.candidatos = [aplicacao.candidato for aplicacao in aplicacoes]

    return vagas


def relatorio(request):
    user = request.user

    vagas_por_mes = (
        Vaga.objects.filter(empresa=user)
        .annotate(month=ExtractMonth('data_criacao'))
        .values('month')
        .annotate(total_vagas=Count('id'))
        .order_by('month')
    )

    candidatos_por_mes = (
        Aplicacao.objects.filter(vaga__empresa=user)
        .annotate(month=ExtractMonth('data_aplicacao'))
        .values('month')
        .annotate(total_candidatos=Count('id'))
        .order_by('month')
    )

    vagas_data = [0] * 12
    candidatos_data = [0] * 12

    for item in vagas_por_mes:
        vagas_data[item['month'] - 1] = item['total_vagas']

    for item in candidatos_por_mes:
        candidatos_data[item['month'] - 1] = item['total_candidatos']

    context = {
        'vagas_data': vagas_data,
        'candidatos_data': candidatos_data,
    }
    
    return render(request, 'relatorio.html', context)
