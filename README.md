## Cap 5) Selecionar um Perfil e Convidar

1)  Vamos exibir na nossa página principal (view `index`) a lista de todos os perfis que temos cadastrados. Altere a view `index` para selecionar todos os perfis:

_(por enquanto, utilize o shell para cadastrar novos perfis)_

    def index(request):
        return render(request, 'perfis/index.html', {"perfis":Perfil.objects.all()})

2) Agora atualize o template `index.html` para iterar os perfis e exibir nome e e-mail:

    <!-- connectedin/perfis/templates/perfis/index.html -->
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">

            <title>ConnectedIn</title>
        </head>
        <body>
            <h1>Index</h1>
            {% if perfis %}
                <ul>
                    {% for perfil in perfis %}
                        {{ perfil.nome }} / {{ perfil.email }}
                    {% endfor %}
                </ul>
            {% else %}
                <p>Nenhum Perfil encontrado</p>
            {% endif %}
        </body>
    </html>

3) Vamos criar um link para exibir o perfil a partir do id

    <!-- connectedin/perfis/templates/perfis/index.html -->
    ...
        <ul>
            {% for perfil in perfis %}
                <a href="/perfis/{{perfil.id}}">{{ perfil.nome }}</a> / {{ perfil.email }}
            {% endfor %}
        </ul>

    ...

4) Observe que o caminho do nosso href corresponde ao caminho que definimos no arquivo `urls.py` para a url de nome exibir: `url(r'^perfis/(?P<perfil_id>\d+)$', views.exibir, name='exibir')`. Vamos melhorar nosso código utilizando o nome da url:

    <!-- connectedin/perfis/templates/perfis/index.html -->
    ...
        <ul>
            {% for perfil in perfis %}
                <li>
                    <a href="{% url 'exibir' perfil.id %}">{{ perfil.nome }}</a> / {{ perfil.email }}
                </li>
            {% endfor %}
        </ul>

    ...

Isso evita que precisemos nos preocupar com o caminho para exibir um determinado perfil.

5) Vamos fazer o mesmo no arquivo `perfil.html` e criar um link que aciona a view `convidar`

    <!-- connectedin/perfis/templates/perfis/perfil.html -->
    ...
            <h1>Detalhe Perfil: {{perfil.nome}}</h1>
            <a href="{% url 'convidar' perfil.id %}">convidar</a>
    ...

6) Agora implementaremos a lógica de convite. O que queremos é que um Perfil seja capaz de se conectar com outro, então vamos, na classe `Perfil`, criar o método `convida` que recebe um perfil convidado.

    class Perfil(models.Model):

        ...

        def convida(self, perfil_convidado):
            pass

        ...

7) Atualizamos a view `convidar` para:

    ...
    from django.http.response import HttpResponseRedirect
    from django.core.urlresolvers import reverse
    ...

    def convidar(request, perfil_id):
        
        perfil_a_convidar = Perfil.objects.get(id=perfil_id)

        perfil_logado = get_perfil_logado(request)

        perfil_logado.convida(perfil_a_convidar)

        return HttpResponseRedirect( reverse( 'index' ) )

    ...

8) Por enquanto, precisamos simular um perfil logado. Então vamos criar o médodo `get_perfil_logado` que retorna um perfil previamente cadastrado (utilize o shell do Django). No arquivo `views.py` crie:

    ...
    def __get_perfil_logado(request):
        return Perfil.objects.get(id=3) # troque "3" por um id previamente cadastrado

    ...

9) Nosso método `convida` da classe `Perfil` precisa agora criar um convite que associe o solicitante e o convidado, então vamos criar a classe `Convite` em `models.py`:

    ...
    class Convite(models.Model):
        solicitante = models.ForeignKey(Perfil, related_name="convites_feitos")
        convidado = models.ForeignKey(Perfil, related_name="convites_recebidos")

    ...

e depois alterar o método convida para criar e gravar um convite:

    def convida(self, perfil_convidado):
        Convite(solicitante=self, convidado=perfil_convidado).save()

10) Como criamos uma nova classe, vamos executar novamente o comando syncdb para criar a tabela no banco

    $ python manage.py syncdb

11) Ok, para finalizar vamos escrever alguma lógica que não permita a criação de convites para perfis que já estejam convidados e nem para sim mesmo. Criamos, na classe `Perfil` o método:

    ...
    def is_convidado(self, perfil):
        
        convites_feitos = self.convites_feitos.filter(convidado__id=perfil.id).exists()
        convites_recebidos = self.convites_recebidos.filter(solicitante__id=perfil.id).exists()

        return  convites_feitos or convites_recebidos
    ...

e agora atualizamos o método `convida`:

    def convida(self, perfil_convidado):
        if not self.is_convidado(perfil_convidado) and perfil_convidado != self:
            Convite(solicitante=self, convidado=perfil_convidado).save()

Acesse a funcionalidade no Browser e verifique no Django shell se os convites estão sendo criados corretamente.