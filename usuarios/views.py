from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import UserForm, ProfileForm
from inscripciones.models import Inscripcion


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = request.POST.get('email')
            user.save()
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})


def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo!')
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})


def cerrar_sesion(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('index')


def perfil_publico(request, username):
    usuario = get_object_or_404(User, username=username)
    profile = usuario.profile
    inscripciones = Inscripcion.objects.filter(
        usuario=usuario, estado='CON'
    ).select_related('torneo')
    return render(request, 'usuarios/perfil_publico.html', {
        'profile': profile,
        'usuario': usuario,
        'inscripciones': inscripciones,
    })


@login_required
def ver_perfil(request):
    profile = request.user.profile
    inscripciones = Inscripcion.objects.filter(usuario=request.user).exclude(estado='CAN').select_related('torneo')
    return render(request, 'usuarios/perfil.html', {
        'profile': profile,
        'inscripciones': inscripciones,
    })


@login_required
def editar_perfil(request):
    profile = request.user.profile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('ver_perfil')
        else:
            messages.error(request, 'Corregí los errores del formulario.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'usuarios/editar_perfil.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })