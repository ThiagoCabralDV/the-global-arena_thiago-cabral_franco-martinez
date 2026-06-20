from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # 1. Creamos el objeto usuario en memoria sin guardarlo en la BD todavía
            user = form.save(commit=False)
            
            # 2. Capturamos el valor del input "email" que pusimos en el HTML
            user.email = request.POST.get('email')
            
            # 3. Ahora sí, guardamos el usuario con el mail incluido en la BD
            user.save()
            
            # Autologueo y redirección (Tu lógica original perfecta)
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