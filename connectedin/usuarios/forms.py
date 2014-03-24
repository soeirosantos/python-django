from django import forms

from django.contrib.auth.models import User

class RegistrarUsuarioForm(forms.Form):
    
    nome = forms.CharField(required=True)
    email = forms.EmailField(required=False)
    senha = forms.CharField(required=False)
    telefone = forms.CharField(required=True)
    nome_empresa = forms.CharField(required=True)

    def add_error(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.util.ErrorList())
        errors.append(message)

    def is_valid(self):
        valid = True
        if not super(RegistrarUsuarioForm, self).is_valid():
            self.add_error("Por favor, verifique os dados informados")
            valid = False

        user_exists = User.objects.filter(username=self.data['email']).exists()

        if user_exists:
            self.add_error("Usuario ja existente")
            valid = False

        return valid