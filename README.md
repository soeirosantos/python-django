## Cap 8) Registrando usuários e criando perfis

1) No capítulo anterior finalizamos a parte de nossa aplicação relacionada a interação entre perfis. Agora vamos cuidar do registro de novos usuários/perfis para que possamos tornar nossa aplicação realmente funcional. Mantendo o foco em modularização, vamos criar uma nova app do Django para cuidar somente dos aspectos relacionados aos usuários:

    $ python manage.py startapp usuarios

(Não esqueça de incluir essa nova app na variável INSTALLED_APPS do arquivo `connectedin/connectedin/settings.py`)

2) Vamos iniciar definindo um mapeamento de url para a tela de registro de usuários. Crie o arquivo `connectedin/usuarios/urls.py` com o seguinte conteúdo:
    
    from django.conf.urls import patterns, url

    urlpatterns = patterns('',
        url(r'^registrar/$', ???, name="registrar"),
    )

Não se esqueça, também, de incluir esse arquivo de urls no arquivo `connectedin/connectedin/urls.py`:

    urlpatterns = patterns('',
        url(r'^', include('perfis.urls')),
        url(r'^', include('usuarios.urls')),
        ...
    )

3) Observe que deixamos com alguns pontos de interrogação o parâmetro onde normalmente informamos nossa função de view. Dessa vez, ao invés de utilizar uma função de view, usaremos uma _class-based view_. Para, isso, simplesmente crie no arquivo `connectedin/usuarios/views.py` uma classe chamada `RegistrarUsuarioView` que extenda a classe `django.views.generic.base.View`:

    from django.views.generic.base import View

    class RegistrarUsuarioView(View):
        pass

4) Vamos definir nessa classe dois métodos para tratar as requisições feitas a nossa view:

    from django.views.generic.base import View

    class RegistrarUsuarioView(View):
        
        def get(self, request, *args, **kwargs):
            pass

        def post(self, request, *args, **kwargs):
            pass

Uma requisição à url que definimos no passo __2__ utilizando o método `HTTP GET` irá acionar nosso método `get`, que será utilizado para exibir a página de registro de usuários. Já uma requisição utilizando `HTTP POST` irá acionar o método `post` responsável por processar os dados enviados pelo formulário na tela e executar as operações necessárias.

5) Precisamos, então, de um template para exibir a página com o formulário que irá receber os dados do usuário. Antes de mais nada vamos criar um template base para nossa aplicação, assim como fizemos na app `perfis`. Assim, crie um template base para aplicação usuarios (`connectedin/usuarios/templates/usuarios/base.html`) conforme abaixo:

    {% load staticfiles %}

    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>ConnectedIn</title>
          
        <link href="{% static "styles/bootstrap.css" %}" rel="stylesheet">
        <link href="{% static "styles/signin.css" %}" rel="stylesheet">

      </head>

      <body>
        <div class="container">
          {% block body %}

          {% endblock %} 
        </div>  
         <script src="{% static "scripts/vendor/bootstrap-min.js" %}"></script>
      </body>
    </html>

6) Agora vamos escrever o código da página que exibirá o formulário. Crie o arquivo `connectedin/usuarios/templates/usuarios/registrar.html`:

    {% extends "usuarios/base.html" %}

    {% block body %}
          
      <form class="form-signin" role="form" action="{% url 'registrar' %}" method="post">
        {% csrf_token %}

        <h2 class="form-signin-heading">Crie seu usuário</h2>

        <input type="text" id="id_email" name="email" class="form-control" placeholder="Email *" required autofocus>
        
        <input type="password" id="id_senha" name="senha" class="form-control"  placeholder="Senha *" required>

        <hr />

        <input type="text" id="id_nome" name="nome" class="form-control" placeholder="Nome *" required >

        <input type="text" id="id_telefone" name="telefone" class="form-control" placeholder="Telefone">

        <input type="text" id="id_nome_empresa" name="nome_empresa" class="form-control" placeholder="Empresa">

        <hr />

        <button class="btn btn-lg btn-primary btn-block" type="submit" value="Login">Registrar</button>

      </form>

    {% endblock %}

7) Vamos atualizar nossos métodos `get` e `post` para renderizar esse template. Nossa view fica assim:

    from django.views.generic.base import View

    from django.shortcuts import render

    class RegistrarUsuarioView(View):

        template_name = 'usuarios/registrar.html'
        
        def get(self, request, *args, **kwargs):
            return render(request, self.template_name)

        def post(self, request, *args, **kwargs):
            return render(request, self.template_name)

Com isso já podemos visualizar nossa página, apenas altere a o arquivo `connectedin/usuarios/urls.py` e adicione nossa view:
    
    from django.conf.urls import patterns, url
    
    from usuarios.views import RegistrarUsuarioView

    urlpatterns = patterns('',
        url(r'^registrar/$', RegistrarUsuarioView.as_view(), name="registrar"),
    )

8) Finalmente, precisamos receber os dados enviados pelo formulário e processá-los no método `post`. Para fazer isso vamos usar um _form_ do Django, uma classe que possa fazer a ligação entre cada um dos campos do nosso template:

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

9) Aqui aparece a classe `django.contrib.auth.models.User` da API responsável por autenticação e autorização de usuários no Django. Nós utilizaremos esta classe como model para guardar os dados dos nossos usuários. Vamos criar o relacionamento que vincula nosso `Perfil` à classe `User`:

    ...
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

    ...

Observe que removemos o atributo email e estamos delegando ao atributo email da classe `User`

9) Atualizamos o método `post` da nossa view para processar o formulário:

    ...

    from usuarios.forms import RegistrarUsuarioForm
    from django.http import HttpResponseRedirect
    from django.contrib.auth.models import User
    from perfis.models import Perfil

    class RegistrarUsuarioView(View):
        
        ...

        def post(self, request, *args, **kwargs):
            form = RegistrarUsuarioForm(request.POST)
            
            if form.is_valid():

                dados_form = form.data
                
                usuario = User.objects.create_user(dados_form['email'], dados_form['email'], dados_form['senha'])            
            
                perfil = Perfil(nome=dados_form['nome'], 
                                email=dados_form['email'], 
                                telefone=dados_form['telefone'],
                                nome_empresa=dados_form['nome_empresa'],
                                usuario=usuario)

                perfil.save()

                return HttpResponseRedirect( reverse('login') )

            return render(request, self.template_name, {'form': form})

Repare que, pelo que vimos até aqui, o retorno do nosso método `post` faz um `HttpResponseRedirect` para um suposto mapeamento de url `login`, que nós não temos ainda, certo? Não se preocupe com isso agora, após cadastrar um usuário será exibida uma mensagem de erro que nós iremos resolver no próximo capítulo.

10) Agora fazemos a ligação entre o template e o nosso formulário:

    ...

      <form class="form-signin" role="form" action="{% url 'registrar' %}" method="post">
        {% csrf_token %}

        <h2 class="form-signin-heading">Crie seu usuário</h2>

        <input type="text" id="id_email" name="email" value="{{form.data.email}}" class="form-control" placeholder="Email *" required autofocus>
        
        <input type="password" id="id_senha" name="senha" value="{{form.data.senha}}" class="form-control"  placeholder="Senha *" required>

        <hr />

        <input type="text" id="id_nome" name="nome" value="{{form.data.nome}}" class="form-control" placeholder="Nome *" required >

        <input type="text" id="id_telefone" name="telefone" value="{{form.data.telefone}}" class="form-control" placeholder="Telefone">

        <input type="text" id="id_nome_empresa" name="nome_empresa" value="{{form.data.nome_empresa}}" class="form-control" placeholder="Empresa">

        <hr />

        <button class="btn btn-lg btn-primary btn-block" type="submit" value="Login">Registrar</button>
        
        <hr />

        {% if form.errors %}
          <div class="alert alert-danger">
            <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
            {{form.non_field_errors}}
          </div>
        {% endif %}

      </form>

    ...