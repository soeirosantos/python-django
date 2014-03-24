## Cap 3) Modelo + Mapeamento

1) Criando o modelo: no arquivo `connectedin/perfis/models.py` vamos criar a classe `Perfil` que vai conter os dados e comportamentos dos nossos perfis. E, aproveitamos para já adicionar alguns atributos.

    ...

    class Perfil(models.Model):
        
        nome = models.CharField(max_length=255, null=False)
        email = models.CharField(max_length=255, null=False)     
        telefone = models.CharField(max_length=15, null=True)
        nome_empresa = models.CharField(max_length=255, null=True)

2) Vamos gerar as tabelas do banco de dados a partir da definição da classe:

    $ python manage.py syncdb

(observe que ele cria outras tabelas referentes a outras aplicações que temos instaladas `settings.py > INSTALLED_APPS`)

Onde foram criadas as tabelas? O Django está usando uma configuração padrão (`settings.py > DATABASES`) para um banco sqlite, veremos como customizar essa configuração mais a frente.

3) Vamos acessar o shell do django e trabalhar um pouco com os métodos que são criados dinamicamente para o nosso model

    $ python manage.py shell

    $ from perfis.models import Perfil

Incluindo:

    $ p = Perfil(nome="Oswaldo", email="oswaldo@gmail.com")

    $ p.save()

Lendo um:

    $ p = Perfil.objects.get(id=1)

Atualizando:

    $ p.nome = "Oswaldo alterado"

    $ p.save()

Lendo vários:
    
    $ Perfil.objects.all()

Vamos utilizar esses métodos para construir nossas funcionalidades.