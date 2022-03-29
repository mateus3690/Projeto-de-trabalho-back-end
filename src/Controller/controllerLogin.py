from database.dbase import ComponenteDB
from utils.validadoresCampos import ValidaCampo
from flask_restful import Resource
from flask import request
#from flask_httpauth import HTTPBasicAuth
from config.configAuth import crypMD5#, AuthSystem

# auth = HTTPBasicAuth()
# @auth.verify_password
# def verifySistem(login, password):
#     return AuthSystem(login=login, password=password)
class DirectLogin(Resource):

     def get(self, email, senha):

          try: 
               condicao = f"email='{email}' and senha='{crypMD5(senha + 'TFHKKFJSTOJ8F')}'"

               usuario = ComponenteDB(nomeTabela='tb_usuario', condicoesDeConsulta=condicao)
               usuario = usuario.consultarDados()

               response = [{
                    'id':         dados[0],
                    'nome':       dados[1],
                    'cpf':        str(dados[2]),
                    'nascimento': str(dados[3]),
                    'email':      str(dados[4]),
                    'salario':    str(dados[6])  
               } for dados in usuario]

               if response == []:
                    response = {
                         "status": "Error",
                         "mensagem":"Registro de usuário não encontrado!"
                         } 
               return response[0]

          except AttributeError:
               response = {
                    'status':'Error',
                    'mensagem':f"Usuário, não existe nos registros"
               }  

          return response  
     
     def put(self, email, senha):
          try:
               condicao = f"email='{email}' and senha='{crypMD5(senha + 'TFHKKFJSTOJ8F')}'"
               dados = request.json
               payload = {}
               
               #login para atualizar dados
               login = ComponenteDB(nomeTabela='tb_usuario', condicoesDeConsulta=condicao)
               login = login.consultarDados()

               if login != []:

                    if 'nome' in dados:
                         payload['nome'] = f"'{dados['nome']}'"
                    
                    if 'nascimento' in dados:
                         payload['nascimento'] = f"'{dados['nascimento']}'"
                    
                    if 'senha' in dados:
                         payload['senha'] = f"'{crypMD5(dados['senha'] + 'TFHKKFJSTOJ8F')}'"

                    if 'salario' in dados:
                         payload['salario'] = f"{dados['salario']}"     
                    
                    pontoDeTrabalho = ComponenteDB(nomeTabela='tb_usuario',
                                                  valorColunaAtualizar = payload, 
                                                  condicoesDeConsulta=condicao,
                                                  salvar=True)

                    pontoDeTrabalho.atualizarDados()

                    response = {
                         'status':'OK',
                         'mensagem':"Dados foram atualizados com sucesso!"
                    }
               
               else:
                    response = {
                              'status':'Error',
                              'mensagem':"Verifique sua credências de login, e tente novamente!"
                    }

          except TypeError:
               response = {
                    'status':'Error',
                    'mensagem':"Null"
               }

          return response

     def delete(self, email, senha):
          try:
               pontoDeTrabalho = ComponenteDB(nomeTabela='tb_usuario', 
                                              condicoesDeConsulta=f"email = '{email}' and senha = '{crypMD5(senha + 'TFHKKFJSTOJ8F')}'",
                                              salvar=True)
               pontoDeTrabalho.apagaDados()

               response = {
                    'status':'Ok',
                    'mensagem':f'O Usuário foi deletado dos registros'
               }
          except AttributeError:
               response = {
                    'status':'Error',
                    'mensagem':'Informe um registro de usuário existente'
               }
          
          return response


class DirectLoginPass(Resource):
     
     # @auth.login_required
     def get(self):

          usuario = ComponenteDB(nomeTabela='tb_usuario')
          usuario = usuario.consultarDados()

          response = [{
                    'id':         dados[0],
                    'nome':       dados[1],
                    'nascimento': str(dados[2]),
                    'cpf':        str(dados[3]),
                    'email':      str(dados[4]),
                    'salario':    str(dados[6])  
               } for dados in usuario]

          if response == []:
                response = {
                     "status": "Error",
                     "mensagem":"Nenhum registro de usuário no momento!"
               }
          
          return response


     def post(self):
          
          try:
               
               dados = request.json
               analiseCpf = ValidaCampo(cpf=dados['cpf'])
               analiseEmail = ValidaCampo(email=dados['email'])

               if analiseCpf.analisaCPF() == True and analiseEmail.analisaEmail() == True:
                    usuario = ComponenteDB(nomeTabela='tb_usuario', 
                                                   inserirColunas={
                                                                      "nome":       f"'{dados['nome']}'",
                                                                      "nascimento": f"'{dados['nascimento']}'",
                                                                      "cpf":        f"'{dados['cpf']}'",
                                                                      "email":      f"'{dados['email']}'",
                                                                      "senha":      f"'{crypMD5(dados['senha'] + 'TFHKKFJSTOJ8F')}'",
                                                                      "salario":    f"{dados['salario']}"
                                                  }, salvar=True)
                    if usuario.inserirDados() == False:
                         response = {
                              'status':'Error',
                              'mensagem':f"Usuário já está registado no sistema!"
                    }
                    else:
                         usuario.inserirDados()
                         response = {
                                   "nome":       f"{dados['nome']}",
                                   "nascimento": f"{dados['nascimento']}",
                                   "cpf":        f"{dados['cpf']}",
                                   "email":      f"{dados['email']}",
                                   "salario":    f"{dados['salario']}"
                         }

               elif analiseCpf.analisaCPF() == False:
                    response = {
                         'status':'Error',
                         'mensagem':'CPF inválido!'
                    }

               elif analiseEmail.analisaEmail() == False:
                    response = {
                         'status':'Error',
                         'mensagem':'Email inválido!'
                    }
          except KeyError:
               response = {
                    'status':'Error',
                    'mensagem':'Falta informação no registro'
               }
          
          except TypeError:
               response = {
                    'status':'Error',
                    'mensagem':'Null'
               }
          return response
               