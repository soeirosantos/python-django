from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader
from perfis.models import Perfil, Convite

from django.http.response import HttpResponseRedirect

from django.core.urlresolvers import reverse

from django.http import Http404

def index(request):
	return render(request, 'perfis/index.html', 
					{"perfis":Perfil.objects.all(), 
					 "perfil_logado":__get_perfil_logado(request)})

def exibir(request, perfil_id):
    perfil = get_object_or_404(Perfil, id=perfil_id)

    perfil_logado = __get_perfil_logado(request)
    is_conectado = perfil in perfil_logado.contatos.all()
    
    return render(request, 'perfis/perfil.html',{'perfil': perfil, 'is_conectado': is_conectado})

def convidar(request, perfil_id):
        
    perfil_a_convidar = get_object_or_404(Perfil, id=perfil_id)

    perfil_logado = __get_perfil_logado(request)

    perfil_logado.convida(perfil_a_convidar)

    return HttpResponseRedirect( reverse('index') )

def aceitar(request, convite_id):
    convite = get_object_or_404(Convite, id=convite_id)
    convite.aceita()
    return HttpResponseRedirect( reverse('index') )

def __get_perfil_logado(request):
        return get_object_or_404(Perfil, id=3) # troque "3" por um id previamente cadastrado