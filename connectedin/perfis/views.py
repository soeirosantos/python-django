from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from perfis.models import Perfil

def index(request):
    return render(request, 'perfis/index.html')

def exibir(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    return render(request, 'perfis/perfil.html',{'perfil': perfil})

def convidar(request, perfil_id):
    return HttpResponse("Convidando perfil: %s" % perfil_id)

def aceitar(request, convite_id):
    return HttpResponse("Aceitando convite: %s" % convite_id)