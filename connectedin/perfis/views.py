from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from perfis.models import Perfil

from django.http.response import HttpResponseRedirect

from django.core.urlresolvers import reverse

def index(request):
	return render(request, 'perfis/index.html', 
					{"perfis":Perfil.objects.all(), 
					 "perfil_logado":__get_perfil_logado(request)})

def exibir(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    return render(request, 'perfis/perfil.html',{'perfil': perfil})

def convidar(request, perfil_id):
        
    perfil_a_convidar = Perfil.objects.get(id=perfil_id)

    perfil_logado = __get_perfil_logado(request)

    perfil_logado.convida(perfil_a_convidar)

    return HttpResponseRedirect( reverse('index') )

def aceitar(request, convite_id):
    return HttpResponse("Aceitando convite: %s" % convite_id)

def __get_perfil_logado(request):
    return Perfil.objects.get(id=3) # troque "3" por um id previamente cadastrado