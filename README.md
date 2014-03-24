## Cap 4) Templates e MVP

1) Vamos fazer nossas views utilizarem templates HTML ao invés de escrever diretamente a resposta como estamos fazendo até agora. Para isso, criamos o diretório `connectedin/perfis/templates`. Dentro do diretório `templates` vamos criar um diretório chamado `perfis`, onde colocaremos nossos arquivos HTML. 

(O Django irá procurar uma pasta chamada templates para carregar os templates em cada aplicação; e ao carregar os templates ele irá registrá-los a partir do caminho relativo a essa pasta, por isso é uma boa prática criarmos essa pasta interna com o mesmo nome da aplicação.)

2) Vamos criar os arquivos `connectedin/perfis/templates/perfis/index.html` para exibir o conteúdo de nossa página principal e `connectedin/perfis/templates/perfis/perfil.html` para exibir os detalhes de um perfil, com os seguintes conteúdos, respectivamente:
    
    <!-- connectedin/perfis/templates/perfis/index.html -->
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">

            <title>ConnectedIn</title>
        </head>
        <body>
            <h1>Index</h1>
        </body>
    </html>
-
    <!-- connectedin/perfis/templates/perfis/perfil.html -->
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">

            <title>ConnectedIn</title>
        </head>
        <body>
            <h1>Detalhe Perfil</h1>
        </body>
    </html>

3) Vamos alterar nossas views para exibir o conteúdo desses templates. Modifique o código do arquivo `connectedin/perfis/views.py` para, ao invés de imprimir uma String, renderizar o template desejado, conforme abaixo:

    ...
    from django.template import RequestContext, loader
    
    def index(request):

        template = loader.get_template('perfis/index.html')
        context = RequestContext(request)

        return HttpResponse(template.render(context))

    ...

4) O objeto context é utilizado para enviarmos dados para o nosso template. Vamos fazer isso na view `exibir`, enviando um perfil que vamos obter a partir do banco de dados:

    ...

    def exibir(request, perfil_id):

        perfil = Perfil.objects.get(id=perfil_id)

        template = loader.get_template('perfis/perfil.html')
    
        context = RequestContext(request, {
            'perfil': perfil,
        })

    return HttpResponse(template.render(context))
    ...

Adicione o import `from perfis.models import Perfil` no topo do arquivo

5) Agora altere o template `perfil.html` para exibir o nome do perfil que estamos obtendo do banco:

    <!-- connectedin/perfis/templates/perfis/perfil.html -->
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">

            <title>ConnectedIn</title>
        </head>
        <body>
            <h1>Detalhe Perfil: {{perfil.nome}}</h1>
        </body>
    </html>

6) Renderizar templates é algo que fazemos o tempo todo, então o Django oferece uma função _shortcut_ que simplifica o código que utilizamos anteriormente. Para isso, basta importarmos a função `render` do módulo `django.shortcuts` e alterar nosso código para:

    ...

    from django.shortcuts import render
    ...
    
    def index(request):
        return render(request, 'perfis/index.html')

    def exibir(request, perfil_id):
    
        perfil = Perfil.objects.get(id=perfil_id)
    
        return render(request, 'perfis/perfil.html',{'perfil': perfil})

    ...
