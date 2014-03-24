from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15, null=True)
    nome_empresa = models.CharField(max_length=255, null=True)

    contatos = models.ManyToManyField('self')

    usuario = models.OneToOneField(User, related_name="perfil")

    @property
    def email(self):
        return self.usuario.email

    def convida(self, perfil_convidado):
        if not self.is_convidado(perfil_convidado) and perfil_convidado != self:
            Convite(solicitante=self, convidado=perfil_convidado).save()

    def is_convidado(self, perfil):
        
        convites_feitos = self.convites_feitos.filter(convidado__id=perfil.id).exists()
        convites_recebidos = self.convites_recebidos.filter(solicitante__id=perfil.id).exists()

        return  convites_feitos or convites_recebidos

class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil, related_name="convites_feitos")
    convidado = models.ForeignKey(Perfil, related_name="convites_recebidos")

    def aceita(self):
        self.convidado.contatos.add(self.solicitante)
        self.delete()