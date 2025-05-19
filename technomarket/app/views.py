from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'app/home.html')

def galeria(request):
    return render(request,'app/galeria.html')

def contacto(request):
    return render(request,'app/contacto.html')

def sobre_nosotros(request):
    return render(request, 'app/sobre_nosotros.html')

def horario(request):
    return render(request,'app/horario.html')

def sesion(request):
    return render(request,'app/sesion.html')
