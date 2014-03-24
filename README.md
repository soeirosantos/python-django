## Cap 6) Layout e melhorias na View

1) Antes de exibir nossa lista de convites, vamos copiar os arquivos css e código html que compõe o layout da nossa rede social. 

* crie a pasta `connectedin/perfis/static`;
* baixe o arquivo %%ARQUIVO%% e;
* copie todo o conteúdo da pasta `static` para a pasta `static` que acabamos de criar

2) Para não termos que aplicar todas as definições de layout, template por template, vamos criar um arquivo base para o nosso layout. Assim, crie o arquivo `connectedin/perfis/templates/perfis/base.html` com o seguinte conteúdo:

    {% load staticfiles %}
    <!DOCTYPE html>
    <html lang="en">
      <head>
        {% block header %}
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">

            <title>ConnectedIn</title>

            <link href="{% static "styles/bootstrap.css" %}" rel="stylesheet">
            <link href="{% static "styles/main.css" %}" rel="stylesheet">
        {% endblock %}
      </head>
      <body>
        <div class="container">
          <div class="header">
            <ul class="nav nav-pills pull-right">
              <li class=""><a href="{% url 'index' %}">Nome</a></li>
              <li class=""><a href="/logout/">Logout</a></li>
            </ul>
            <h3 class="text-muted">ConnectedIn</h3>
          </div>

          <div class="row content">
                {% block body %}

                {% endblock %}        
          </div>
        </div>
        <script src="{% static "scripts/vendor/bootstrap-min.js" %}"></script>
      </body>
    </html>

3) Agora atualize o conteúdo do arquivo `index.html`, adicionando algum código html e, principalmente, estendendo o nosso layout base:

    {% extends "perfis/base.html" %}

    {% block body %}

    <div class="col-lg-12">

        <div class="panel panel-default">
            <div class="panel-heading">
                <strong>Todos os Perfis</strong>
            </div>
            {% if perfis %}
                <ul class="list-group">
                    {% for perfil in perfis %}
                        <a href="{% url 'exibir' perfil.id %}" class="list-group-item">{{ perfil.nome }} // {{ perfil.email }}</a>
                    {% endfor %}
                </ul>
            {% else %}
                <div class="panel-body">
                    <p>Nenhum Perfil encontrado</p>
                </div>
            {% endif %}
        </div>

    </div>

    {% endblock %}

4) Faça o mesmo com o arquivo `perfil.html`:

    {% extends "perfis/base.html" %}

    {% block body %}
    {% load staticfiles %}

    <div class="row">
        <div class="col-lg-12">
            <h2 style="margin-top:0">{{perfil.nome}}</h2>
            <address>
              <strong>{{perfil.nome_empresa}}</strong><br>
              <abbr title="Telefone">Tel:</abbr> {{perfil.telefone}}<br>
              <a href="mailto:{{profile.email}}">{{profile.email}}</a>
            </address>
            <a href="{% url 'convidar' perfil.id %}">convidar</a>
        </div>
    </div>

    {% endblock %}

5) Agora estamos preparados para exibir nossa lista de convites. No template `index.html` construa um bloco de código html semelhante ao que utilizamos para exibir __Todos os Perfis__ só que com as devidas alterações:

    <div class="panel panel-default">
        {% if perfil_logado.convites_recebidos.count %}
            <div class="panel-heading">
                <strong>Convites aguardando aprovação</strong>
            </div>
            <ul class="list-group">
                {% for convite in perfil_logado.convites_recebidos.all %}
                    <li class="list-group-item">
                            {{ convite.solicitante.nome }} 
                            <a href="{% url 'aceitar' convite.id %}" class="pull-right">aceitar</a>
                    </li>
                {% endfor %}
            </ul>
        {% else %}
            <div class="panel-body">
                <p>Nenhum convite recebido :(</p>
            </div>
        {% endif %}
    </div>

6) Como podemos ver nosso template está esperando receber o perfil_logado, então vamos atualizar nossa view `index`: 

    def index(request):
        return render(request, 'perfis/index.html', {"perfis":Perfil.objects.all(), "perfil_logado":__get_perfil_logado(request)})

7) Utilize o shell para criar convites para o seu perfil

    $ from perfis.models import Convite, Perfil
    $ a_convidar = Perfil.objects.get(id=3) # utilize o mesmo id que vc fixou no __get_perfil_logado()
    $ solicitante = Perfil.objects.get(id=4)
    $ solicitante.convida(a_convidar)

8) Vamos melhorar um pouco a apresentação da nossa lista de convites através de um filtro de templates do Django. Primeiro, vamos alterar o cabeçalho do nosso painel de convites conforme abaixo:
        
    ...
    <div class="panel-heading">
        <strong>Você tem {{perfil_logado.convites_recebidos.count}} convites aguardando aprovação</strong>
    </div>
    ...

Agora, se tivermos um único convite não queremos que a palavra _convites_ fique no plural. Então aplicamos o filtro `pluralize`:
    
    ...
    <div class="panel-heading">
        <strong>Você tem {{perfil_logado.convites_recebidos.count}} convite{{ perfil_logado.convites_recebidos.count|pluralize }} aguardando aprovação</strong>
    </div>
    ...

Se olharmos para o nosso painel de convites inteiro agora, veremos que estamos usando a expressão `perfil_logado.convites_recebidos.count` muitas vezes. Vamos melhorar isso adicionando uma variável para o total de convites em um bloco `with`:

    <div class="panel panel-default">
        {% with total_de_convites=perfil_logado.convites_recebidos.count %}
            {% if total_de_convites %}
                <div class="panel-heading">
                        <strong>Você tem {{total_de_convites}} convite{{ total_de_convites|pluralize }} aguardando aprovação</strong>
                </div>
                <ul class="list-group">
                    {% for convite in perfil_logado.convites_recebidos.all %}
                        <li class="list-group-item">
                                {{ convite.solicitante.nome }} 
                                <a href="{% url 'conectar' convite.id %}" class="pull-right">aceitar</a>
                        </li>
                    {% endfor %}
                </ul>
            {% else %}
                <div class="panel-body">
                    <p>Nenhum convite recebido :(</p>
                </div>
            {% endif %}
        {% endwith %}
    </div>