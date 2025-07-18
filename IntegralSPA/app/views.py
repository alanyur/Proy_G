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

User = get_user_model()

# Pagina principal, muestra los servicios disponibles
def home(request):
    servicios = Servicio.objects.all()
    return render(request, 'app/home.html', {'servicios': servicios})

# Pagina que muestra la galeria de trabajos realizados
def galeria(request):
    return render(request, 'app/galeria.html')

# Pagina para enviar una solicitud de servicio
def contacto(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    usuario = request.user

    # Si es post crea la solicitud
    if request.method == 'POST':
        mensaje = request.POST.get('mensaje')
        Solicitud.objects.create(
            cliente=usuario,
            servicio=servicio,
            descripcion=mensaje,
            estado='pendiente'
        )

        # Da mensaje de exito
        messages.success(request, 'Solicitud enviada correctamente.')
        return redirect('home')

    return render(request, 'app/contacto.html', {
        'servicio': servicio,
        'usuario': usuario
    })

# Pagina que muestra la disponibilidad horaria de los trabajadores
def horario(request):

    # Usa un diccionario para organizar la disponpibilidad por trabajador y dia
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

# Pagina de inicio de sesion
def sesion(request):
    return render(request, 'app/sesion.html')

# Pagina de registro
def registro(request):
    return render(request, 'app/registro.html')

# Maneja el inicio de sesion de usuarios, redirige segun rol, da mensajes de error o exito
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

                    # Redirige segun rol
                    if user.rol == 'admin':
                        messages.success(request, 'Bienvenido administrador.')
                        return redirect('home')
                    elif user.rol == 'trabajador':
                        messages.success(request, 'Bienvenido trabajador.')
                        return redirect('home')
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

# Cierra la sesion del usuario
def cerrar_sesion(request):
    logout(request)
    return redirect('sesion')

# Maneja el registro de los usuarios
def registro_succes(request):

    # Si es post crea al usuario con los datos recibidos
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

def edit(request):
    if request.method == 'POST':
        if 'eliminar' in request.POST:
            solicitud_id = request.POST['eliminar']
            Solicitud.objects.filter(id=solicitud_id).delete()
        elif 'marcar_listo' in request.POST:
            solicitud_id = request.POST['marcar_listo']
            solicitud = Solicitud.objects.get(id=solicitud_id)
            if solicitud.estado == 'pendiente':
                solicitud.estado = 'listo'
                solicitud.save()
        return redirect('edit')

    solicitudes = Solicitud.objects.all()
    return render(request, 'app/edit.html', {'solicitudes': solicitudes})