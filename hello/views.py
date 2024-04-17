from django.shortcuts import render
from django.http import HttpResponse
from .models import CaObject, CaEntityLabel

# Create your views here.

def objects(request):
    return HttpResponse("Hello, World!\nThis is new")

def home(request):
    objects = CaObject.objects.all()
    return render(request, 'hello/home.html', {'objects': objects})