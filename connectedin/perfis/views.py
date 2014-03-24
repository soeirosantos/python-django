from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Bem-vindo a ConnectedIn!")

def exibir(request, perfil_id):
    return HttpResponse("Exibindo perfil: %s" % perfil_id)

def convidar(request, perfil_id):
    return HttpResponse("Convidando perfil: %s" % perfil_id)

def aceitar(request, convite_id):
    return HttpResponse("Aceitando convite: %s" % convite_id)