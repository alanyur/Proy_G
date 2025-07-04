from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .forms import LoginForm
from django.http import HttpResponse

User = get_user_model()  # ahora usas tu modelo Usuario

def home(request):
    return render(request, 'app/home.html')

def galeria(request):
    return render(request, 'app/galeria.html')

def contacto(request):
    return render(request, 'app/contacto.html')

def horario(request):
    return render(request, 'app/horario.html')

def sesion(request):
    return render(request, 'app/sesion.html')

def registro(request):
    return render(request, 'app/registro.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)

                    # 🔍 Verifica el rol
                    if user.rol == 'admin':
                        messages.success(request, 'Bienvenido administrador.')
                        return redirect('home')  # o redirect('admin_panel') si lo separas
                    elif user.rol == 'trabajador':
                        messages.success(request, 'Bienvenido trabajador.')
                        return redirect('home')  # o alguna vista de gestión de horario
                    elif user.rol == 'cliente':
                        messages.success(request, 'Bienvenido cliente.')
                        return redirect('home')
                else:
                    messages.error(request, 'Cuenta desactivada')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'app/sesion.html', {'form': form})


def cerrar_sesion(request):
    logout(request)
    return redirect('sesion')  # redirige a la vista de login


def registro_succes(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Rut
        email = request.POST.get('email')
        password = request.POST.get('password')
        nombre = request.POST.get('first_name')
        apellido = request.POST.get('last_name')
        telefono = request.POST.get('telefono')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=nombre,
                last_name=apellido,
                telefono=telefono,
                fecha_nacimiento=fecha_nacimiento,
                rol='cliente'
            )
            messages.success(request, 'Usuario registrado correctamente. Ahora inicia sesión.')
            return redirect('sesion')
        except Exception as e:
            messages.error(request, f'Error al registrar usuario: {str(e)}')

    return render(request, 'app/registro.html')

