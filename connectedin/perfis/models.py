from django.db import models

class Perfil(models.Model):
    
    nome = models.CharField(max_length=255)
    email = models.CharField(max_length=255, null=False)     
    telefone = models.CharField(max_length=15, null=True)
    nome_empresa = models.CharField(max_length=255, null=True)
