## Cap 2) Hello World + Aplicação

1) Criando a aplicação

    $ python manage.py startapp perfis

2) Adicione a aplicação criada à lista de aplicações do projeto. Para fazer isso altere o arquivo `connectedin/connectedin/settings.py` e adicione o nome da aplicação na tupla __INSTALLED_APPS__.

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'perfis',
    )

3) Podemos, agora, exibir nossa própria mensagem no browser. Então, abra o arquivo `connectedin/perfis/views.py` e adicione uma função que receba um parâmetro chamado request e retorne um objeto do tipo HttpResponse:

    from django.http import HttpResponse

    def index(request):
        return HttpResponse("Bem-vindo a ConnectedIn!")

4) Para executarmos nossa view a partir de uma requisição do browser precisamos definir qual URL será acessada. Vamos, então, editar o arquivo `connectedin/connectedin/urls.py` e adicionar o nosso padrão de URL:

    ...
    urlpatterns = patterns('',
       url(r'^$', 'perfis.views.index', name='home'),
        ...
    )

Acesse http://localhost:8000 e veja a mensagem que passamos na resposta.

5) Vamos melhorar um pouco a nossa configuração de URL e trazer a configuração pra dentro da aplicação `perfis`. Vamos criar um arquivo `connectedin/perfis/urls.py` e adicionar o código:

    from django.conf.urls import patterns, url
    from perfis import views

    urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
    )

Agora acesse o arquivo `connectedin/connectedin/urls.py` e atualize o código para incluir o arquivo de URLs da nossa aplicação `perfis`:

    ...
    urlpatterns = patterns('',
        url(r'^', include('perfis.urls')),
        ...
    )
    ...

Verifique no browser que nada mudou, somente melhoramos a modularização do nosso código.

6) Nossa rede social terá, basicamente, quatro funcionalidades:

    * mostrar nossa página principal com os perfis que estamos conectados;
    * mostrar a página de um perfil específico;
    * convidar um perfil a fazer parte da nossa rede;
    * e aceitar um convite

Agora que já sabemos como criar views que podem ser acessadas a partir do browser, vamos criar uma função de view para cada uma dessas funcionalidades. No arquivo `connectedin/perfis/views.py` adicione as seguintes views:

    def exibir(request, perfil_id):
        return HttpResponse("Exibindo perfil: %s" % perfil_id)

    def convidar(request, perfil_id):
        return HttpResponse("Convidando perfil: %s" % perfil_id)

    def aceitar(request, convite_id):
        return HttpResponse("Aceitando convite: %s" % convite_id)

Agora configure as URLs para cada nova view:

    urlpatterns = patterns('',
        ...
          url(r'^perfis/(?P<perfil_id>\d+)$', views.exibir, name='exibir'),
          url(r'^perfis/(?P<perfil_id>\d+)/convidar$', views.convidar, name='convidar'),
          url(r'^convites/(?P<convite_id>\d+)/aceitar$', views.aceitar, name='aceitar'),
    )