from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .forms import LoginForm, SolicitudForm
from django.http import HttpResponse
from .models import Servicio, Solicitud
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from .models import Disponibilidad

User = get_user_model()  # ahora usas tu modelo Usuario

def home(request):
    servicios = Servicio.objects.all()
    return render(request, 'app/home.html', {'servicios': servicios})

def galeria(request):
    return render(request, 'app/galeria.html')

def contacto(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    usuario = request.user

    if request.method == 'POST':
        mensaje = request.POST.get('mensaje')
        Solicitud.objects.create(
            cliente=usuario,
            servicio=servicio,
            descripcion=mensaje,
            estado='pendiente'
        )
        messages.success(request, 'Solicitud enviada correctamente.')
        return redirect('home')

    return render(request, 'app/contacto.html', {
        'servicio': servicio,
        'usuario': usuario
    })

def horario(request):
    disponibilidades = defaultdict(list)
    for d in Disponibilidad.objects.select_related("trabajador"):
        disponibilidades[d.dia].append({
            "trabajador": f"{d.trabajador.first_name} {d.trabajador.last_name}",
            "inicio": d.hora_inicio.strftime("%H:%M"),
            "fin": d.hora_fin.strftime("%H:%M"),
        })
    return render(request, "app/horario.html", {
        "disponibilidades": dict(disponibilidades)
    })

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

