from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request,'app/home.html')

def galeria(request):
    return render(request,'app/galeria.html')

def contacto(request):
    return render(request,'app/contacto.html')

def horario(request):
    return render(request,'app/horario.html')

def sesion(request):
    return render(request,'app/sesion.html')

def registro(request):
    return render(request,'app/registro.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['passsword'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated succes') 
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})            

def registro_succes(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)  # Autentica automáticamente
            return redirect('home')  # Redirige a home tras éxito
        except Exception as e:
            return render(request, 'app/registro.html', {
                'error': f'Error: {str(e)}'
            })
    
    return render(request, 'app/registro.html')
    
