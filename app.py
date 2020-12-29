from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

# USUARIOS = {                        Usado para simular a autenticação sem os registros na tabela
#     'Adilson':'123',
#     'Rafael':'456',
# }
#
# @auth.verify_password      # Não tem os parenteses por não ser uma função
# def verificacao(login, senha):
#     # print('validando usuario')     # Usamos apenas para verificar se está retornando verdadeiro ou falso
#     # print(USUARIOS.get(login) == senha)
#     if not (login, senha):
#         return False
#     return USUARIOS.get(login) == senha

@auth.verify_password      # Não tem os parenteses por não ser uma função
def verificacao(login, senha):
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first()

class Pessoa(Resource):
    @auth.login_required   # Não tem os parenteses por não ser uma função apenas impoe a passagem do metodo pelo auth
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
            response = {
                'nome' :pessoa.nome,
                'idade' :pessoa.idade,
                'id' :pessoa.id
            }
        except AttributeError:
            response = {
                'status':'error',
                'mensagem':'Pessoa nao encontrada!'
            }
        return response

    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        if 'nome' in dados:
            pessoa.nome = dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        pessoa.save()
        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.idade
        }
        return response

    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        mensagem = 'Pessoa {} excluida com sucesso!'.format(pessoa.nome)
        pessoa.delete()
        return{'status':'sucesso', 'mensagem' :mensagem}

class ListaPessoas(Resource):
    @auth.login_required  # Não tem os parenteses por não ser uma função apenas impoe a passagem do metodo pelo auth
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'idade':i.idade} for i in pessoas]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade': pessoa.idade,
        }
        return response

class ListaAtividade(Resource):
    def gat(self):
        pass

    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
        atividade.save()
        response = {
            'pessoa':atividade.pessoa.nome,
            'nome':atividade.nome,
            'id':atividade.id
        }
        return response

api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividade, '/atividades/')

if __name__ == '__main__':
    app.run()

