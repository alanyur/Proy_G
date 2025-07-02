from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
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
                    return redirect('home')  # ✅ redirige al home.html
                else:
                    messages.error(request, 'Cuenta desactivada')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'app/sesion.html', {'form': form})

def registro_succes(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)  # Loguea automáticamente tras crear cuenta
            return redirect('home.html')
        except Exception as e:
            messages.error(request, f'Error al registrar usuario: {str(e)}')

    return render(request, 'app/registro.html')
