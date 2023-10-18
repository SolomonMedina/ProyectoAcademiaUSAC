from django.shortcuts import render, HttpResponse
from registro.registro import Registro

def home(request):

    registro=Registro(request)

    return render(request,"AcademiaApp/home.html")




