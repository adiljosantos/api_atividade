from models import Pessoas

# Insere pessoas no banco
def insere_pessoas():
    pessoa = Pessoas(nome='Adilson', idade=59)
    print(pessoa)
    pessoa.save()

# Consulta as pessoas no banco
def consulta_pessoas():
    pessoa = Pessoas.query.all()
    #pessoa = Pessoas.query.filter_by(nome='Rafael').first()
    #print(pessoa.nome, ' ', pessoa.idade)
    for p in pessoa:
        print(p.nome, ' ',p.idade)

#Faz alterações nas pessoas
def altera_pessoas():
    pessoa = Pessoas.query.filter_by(nome='Galeanni').first()
    pessoa.nome = 'Felipe'
    pessoa.save()

#Exclui uma pessoa do banco locslizando pelo nome
def exclui_pessoas():
    pessoa = Pessoas.query.filter_by(nome='Galeanni').first()
    pessoa.delete()

if __name__ == '__main__':
    # insere_pessoas()
    # altera_pessoas()
    # exclui_pessoas()
    consulta_pessoas()