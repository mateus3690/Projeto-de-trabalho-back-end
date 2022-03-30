import repackage
repackage.up()

from database.dbase import ComponenteDB
from utils.calcularHoras import CalculoDoDia as calDia
from utils.buscarDiaSemana import CalendariaSemanal
#from config.auth import AuthSystem
from flask_restful import Resource
from flask import request


# auth = HTTPBasicAuth()
# @auth.verify_password
# def verifySistem(login, password):
#     return AuthSystem(login=login, password=password)


class DirectCalendario(Resource):
     
     def get(self, chave, registro):

          try: 
               condicao = f"chave='{chave}' and registro='{registro}'"
               if registro == 'pass':
                    condicao = f"chave='{chave}' order by 1 desc"

               pontoDeTrabalho = ComponenteDB(nomeTabela='tb_calendario', condicoesDeConsulta=condicao)
               pontoDeTrabalho = pontoDeTrabalho.consultarDados()

               response = [{
                    'id':             dados[0],
                    'id_usuario':     dados[1],
                    'dia_semana':     dados[2],
                    'primeiro_ponto': str(dados[3]),
                    'segundo_ponto':  str(dados[4]),
                    'terceiro_ponto': str(dados[5]),
                    'quarto_ponto':   str(dados[6]),
                    'saldo_dia':      str(dados[7]),
                    'registro':       dados[8],
                    'chave'   :       dados[9]
                    } for dados in pontoDeTrabalho]

               if response == []:
                    response = {"mensagem":"Nenhum registro de ponto no momento"}
          
               return response

          except AttributeError:
               response = {
                    'status':'Error',
                         'mensagem':f"Ponto de trabalho, não existe nos registros"
               }  

          return response  

     def put(self, chave, registro):

          try:
               condicao = f"chave='{chave}' and registro='{registro}'"
               dados = request.json
               payload = {}
               #case para atualizar somente a hora do ponto, sua data não pode mudar, só deletando
               if 'primeiro_ponto' in dados:
                    payload['primeiro_ponto'] = f"'{dados['primeiro_ponto']}'"
                    payload['mes_ano'] = str(dados['primeiro_ponto'][0:7]).replace('-', '')
                    
               if 'segundo_ponto' in dados:
                    payload['segundo_ponto'] = f"'{dados['segundo_ponto']}'"
               
               if 'terceiro_ponto' in dados:
                    payload['terceiro_ponto'] = f"'{dados['terceiro_ponto']}'"
                    
               if 'quarto_ponto' in dados:
                    payload['quarto_ponto'] = f"'{dados['quarto_ponto']}'"     

               #atualizar o novo saldo do dia
               diaSeman = ComponenteDB(nomeTabela='tb_calendario',
                                       valorConsulta="dia_semana",
                                       condicoesDeConsulta=condicao)
               diaSeman = diaSeman.consultarDados()[0]
  
               retornoSaldo = calDia(
                    dados['primeiro_ponto'],
                    dados['segundo_ponto'],
                    dados['terceiro_ponto'],
                    dados['quarto_ponto'],
                    (True if diaSeman[0] == 'Sexta-Feira' else False)
               )
               
               payload['saldo_dia'] = retornoSaldo.saldoDia()
               
               pontoDeTrabalho = ComponenteDB(nomeTabela='tb_calendario',
                                              valorColunaAtualizar = payload, 
                                              condicoesDeConsulta=condicao,
                                              salvar=True)
               pontoDeTrabalho.atualizarDados()

               response = {
                    'status':'OK',
                    'mensagem':"Dados foram atualizados com sucesso!"
               }

          except TypeError:
               response = {
                    'status':'Error',
                    'mensagem':"Null"
               }

          return response
     
     def delete(self, chave, registro):
          
          try:
               pontoDeTrabalho = ComponenteDB(nomeTabela='tb_calendario', 
                                              condicoesDeConsulta=f"chave = '{chave}' and registro = '{registro}'",
                                              salvar=True)
               pontoDeTrabalho.apagaDados()

               response = {
                    'status':'Ok',
                    'mensagem':f'O Ponto foi deletado dos registros'
               }
          except AttributeError:
               response = {
                    'status':'Error',
                    'mensagem':'Informe um registro de pronto existente'
               }
          
          return response


class DirectCalendarioPass(Resource):

     # @auth.login_required
     def get(self):
          pontoDeTrabalho = ComponenteDB(nomeTabela='tb_calendario')
          pontoDeTrabalho = pontoDeTrabalho.consultarDados()

          response = [{
               'id':             dados[0],
               'id_usuario':     dados[1],
               'dia_semana':     dados[2],
               'primeiro_ponto': str(dados[3]),
               'segundo_ponto':  str(dados[4]),
               'terceiro_ponto': str(dados[5]),
               'quarto_ponto':   str(dados[6]),
               'saldo_dia':      str(dados[7]),
               'registro':       dados[8],
               'chave'   :       dados[9]
               } for dados in pontoDeTrabalho]

          if response == []:
                response = {"mensagem":"Nenhum registro de ponto no momento"}
          
          return response

    # @auth.login_required
     def post(self):
          
          try:
               
               dados = request.json
               diaSeman = CalendariaSemanal(dados['primeiro_ponto']) #mask yyyy-mm-dd hh:mm:ss

               registroUnico = str(dados['primeiro_ponto']).split(' ')
               registroUnico = str(registroUnico[0]).replace('-','')
               uniqueChave = int(dados['chave']) + int(registroUnico)

               retornoSaldo = calDia(
                    dados['primeiro_ponto'],
                    dados['segundo_ponto'],
                    dados['terceiro_ponto'],
                    dados['quarto_ponto'],
                    (True if diaSeman.retornaDia() == 'Sexta-Feira' else False)           
               )     
               
               mes_ano = str(dados['primeiro_ponto'][0:7]).replace('-', '')

               id_usuario = ComponenteDB(nomeTabela='tb_usuario', 
                                         valorConsulta="id",
                                         condicoesDeConsulta=f"cpf='{dados['chave']}'")
               id_usuario = id_usuario.consultarDados()[0]

               pontoDeTrabalho = ComponenteDB(nomeTabela='tb_calendario',
                                              inserirColunas={
                                                            'id_usuario':     id_usuario[0],
                                                            'dia_semana':     f"'{diaSeman.retornaDia()}'",
                                                            'primeiro_ponto': f"'{dados['primeiro_ponto']}'",
                                                            'segundo_ponto':  f"'{dados['segundo_ponto']}'",
                                                            'terceiro_ponto': f"'{dados['terceiro_ponto']}'",
                                                            'quarto_ponto':   f"'{dados['quarto_ponto']}'",
                                                            'saldo_dia':      retornoSaldo.saldoDia(),
                                                            'registro':       f"'{uniqueChave}'",
                                                            'chave'   :       f"'{dados['chave']}'",
                                                            'mes_ano':        f"'{mes_ano}'"}, salvar=True)
                                                             
               if pontoDeTrabalho.inserirDados() == False:
                     response = {
                         'status':'Error',
                         'mensagem':f"Ponto de registro '{uniqueChave}', já está registado no sistema!"
                    }
               else:
                    pontoDeTrabalho.inserirDados()
                    response = {
                                   'dia_semana':     f"{diaSeman.retornaDia()}",
                                   'primeiro_ponto': f"{dados['primeiro_ponto']}",
                                   'segundo_ponto':  f"{dados['segundo_ponto']}",
                                   'terceiro_ponto': f"{dados['terceiro_ponto']}",
                                   'quarto_ponto':   f"{dados['quarto_ponto']}",
                                   'saldo_dia':      retornoSaldo.saldoDia(),
                                   'registro':       f"{uniqueChave}",
                                   'chave'   :       f"{dados['chave']}"
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

          except ValueError:
               response = {
                    'status':'Error',
                    'mensagem':'Erro no formato da data'
               }

          return response
          