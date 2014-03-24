## Cap 7) Aceitando Convites e Exibindo nossos Contatos

1) Agora nos resta aceitar os convites que recebemos. Na lista de convites já podemos ver o link para aceitar um convite, que aciona a função `aceitar` do nosso arquivo de views, passando o id do convite. Vamos implementar a lógica de aceitar convites criando o método `aceita` em nossa classe `Perfil`:

    class Convite(models.Model):
        solicitante = models.ForeignKey(Perfil, related_name="convites_feitos")
        convidado = models.ForeignKey(Perfil, related_name="convites_recebidos")

        def aceita(self):
            pass

2) Atualizamos a view `aceitar`, agora, executando o método `aceita` do convite selecionado:

    ...

    def aceitar(request, convite_id):
        convite = Convite.objects.get(id=convite_id)
        convite.aceita()
        return HttpResponseRedirect( reverse( 'index' ) )

    ...

Não esqueça de adicionar o import da classe `Convite`: `from perfis.models import Perfil, Convite`

3) Precisamos relacionar dois perfis, então vamos criar um mapeamento _muitos-para-muitos_ na nossa classe `Perfil`:
    
    ...

    class Perfil(models.Model):
        
        ...
        contatos = models.ManyToManyField('self')

    ...

4) Agora atualize o método `aceita` da classe `Convite`, passando o perfil do solicitante para a lista de contatos de quem foi convidado:
    
    class Convite(models.Model):
        solicitante = models.ForeignKey(Perfil, related_name="convites_feitos")
        convidado = models.ForeignKey(Perfil, related_name="convites_recebidos")

        def aceita(self):
            self.convidado.contatos.add(solicitante)
            self.delete()

5) Como mexemos no mapeamento da classe `Perfil`, precisamos realizar uma nova sincronização com o banco. Só que, como já existe uma tabela criada para esta classe, o Django não vai efetuar as alterações que desejamos. Vamos utilizar a abordagem mais simples possível para o nosso caso e remover o aquivo `connectedin/db.sqlite3` e deixar o Django regerar tudo. 

    $ python manage.py syncdb

(A forma mais adequada de administrar a evolução do banco de dados em relação as alterações no seu modelo é utilizar uma ferramenta de _migrations_. A ferramenta de migrations mais famosa utilizada com o Django é o _South_ [http://south.aeracode.org/]. A partir da versão 1.7, o Django contará com sua própria solução de migrations)

6) O que acontece se tentarmos acessar nossa página principal? Vai ocorrer um erro informando que o perfil que estamos tentando acessar não existe (nesse caso nosso perfil logado). De fato, nós apagamos todo nosso banco de dados. Observe as linhas contidas no erro:
    
    Exception Type: DoesNotExist
    Exception Value: Perfil matching query does not exist.

A exceção `DoesNotExist` é lançada sempre que o Django não consegue encontrar um object relativo a uma query. Nossas outras views também estão suscetíveis a esse mesmo tipo de erro, então vamos aproveitar e dar um tratamento adequado que vai melhorar nosso código em vários pontos:  

    ...
    
    from django.http import Http404

    ...

    def __get_perfil_logado(request):
        try:
            perfil_logado_fake = Perfil.objects.get(id=3)
        except Perfil.DoesNotExist:
            raise Http404

Como esta construção é muito comum, o Django fornece uma função shortcut que economiza algumas linhas: ``


    def __get_perfil_logado(request):
        return get_object_or_404(Perfil, id=3) # troque "3" por um id previamente cadastrado


Adicione o import do shortcut: `from django.shortcuts import render, get_object_or_404`

Agora, atualize as views `exibir`, `convidar` e `aceitar` que também estão suscetíveis ao erro `DoesNotExist`.

(Não se esqueça que nosso método `__get_perfil_logado` ainda está com um comportamento _fake_ que será resolvido em breve, por hora continue usando o shell para criar os perfis e convites)

7) Crie na nossa página principal um painel para listar nossos contatos, que será praticamente idêntico aos outros 2 que já criamos anteriormente.

    <div class="panel panel-default">
        {% with total_de_contatos=perfil_logado.contatos.count %}
            {% if total_de_contatos %}
                <div class="panel-heading">
                        <strong>Você tem {{total_de_contatos}} contato{{ total_de_contatos|pluralize }}</strong>
                </div>
                <ul class="list-group">
                    {% for contato in perfil_logado.contatos %}
                        <a href="{% url 'exibir' contato.id %}" class="list-group-item">{{ contato.nome }} // {{ contato.email }}</a>
                    {% endfor %}
                </ul>
            {% else %}
                <div class="panel-body">
                    <p>Você não possui contatos no momento :(</p>
                </div>
            {% endif %}
        {% endwith %}
    </div>

8) E, por fim, uma última melhoria na exibição de nossas páginas. Observe que no template `perfil.html` mesmo depois de conectados o botão de __convidar__ continua aparecendo. Vamos criar uma condição para sua exibição:
    
    ...
    {% if is_conectado %}
        <div class="well well-sm">Vocês estão conectados!</div>
    {% else %}
        <a href="{% url 'convidar' perfil.id %}"  class="btn btn-success" role="button">convidar</a>
    {% endif %}

    ...

Atualize a função de view `exibir` para verificar se os perfis estão conectados e disponibilizar a variável `is_conectado` para o template.

    def exibir(request, perfil_id):
        perfil = get_object_or_404(Perfil, id=perfil_id)
        
        perfil_logado = __get_perfil_logado(request)
        is_conectado = perfil in perfil_logado.contatos.all()
        
        return render(request, 'perfis/perfil.html',{'perfil': perfil, 'is_conectado': is_conectado})