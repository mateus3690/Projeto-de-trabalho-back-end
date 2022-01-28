from re import A
import repackage
repackage.up()

from config.tables import Calendario
from utils.buscarDiaSemana import CalendariaSemanal
from utils.calcularHoras import CalculoDoDia as calDia
from config.auth import AuthSystem
from flask_restful import Resource
from flask import request
import sqlalchemy
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
@auth.verify_password
def verifySistem(login, password):
    return AuthSystem(login=login, password=password)


class DirectCalendario(Resource):
     
     def get(self, registro):

          try:
               pontoDeTrabalho = Calendario.query.filter_by(registro=f'Registro-{registro}').first()
               response = {
                    'id':             pontoDeTrabalho.id,
                    'dia_semana':     pontoDeTrabalho.dia_semana,
                    'primeiro_ponto': pontoDeTrabalho.primeiro_ponto,
                    'segundo_ponto':  pontoDeTrabalho.segundo_ponto,
                    'terceiro_ponto': pontoDeTrabalho.terceiro_ponto,
                    'quarto_ponto':   pontoDeTrabalho.quarto_ponto,
                    'saldo_dia':      f'{str(pontoDeTrabalho.saldo_dia)}',
                    'registro':       pontoDeTrabalho.registro
               }

          except AttributeError:
               response = {
                    'status':'Error',
                         'mensagem':f"Ponto de trabalho, não existe nos registros"
               }  

          return response      
     
     #@auth.login_required
     def put(self, registro):

          try:
               #buscarID = Calendario.query.filter_by(registro=f'Registro-{registro}').first()
               pontoDeTrabalho = Calendario.query.filter_by(registro=f'Registro-{registro}').first()
               dados = request.json
               
               #case para atualizar somente a hora do ponto, sua data não pode mudar, só deletando
               if 'primeiro_ponto' in dados:
                    novoPonto= {
                         "data":str(pontoDeTrabalho.primeiro_ponto).split(' '),
                         "hora":str(dados['primeiro_ponto']).split(' ')
                    }
                    data = novoPonto['data'][0]
                    hora = novoPonto['hora'][1]

                    pontoDeTrabalho.primeiro_ponto = f'{data} {hora}'
               
               if 'segundo_ponto' in dados:
                    novoPonto= {
                         "data":str(pontoDeTrabalho.segundo_ponto).split(' '),
                         "hora":str(dados['segundo_ponto']).split(' ')
                    }
                    data = novoPonto['data'][0]
                    hora = novoPonto['hora'][1]

                    pontoDeTrabalho.segundo_ponto = f'{data} {hora}'
               
               if 'terceiro_ponto' in dados:
                    novoPonto= {
                         "data":str(pontoDeTrabalho.terceiro_ponto).split(' '),
                         "hora":str(dados['terceiro_ponto']).split(' ')
                    }
                    data = novoPonto['data'][0]
                    hora = novoPonto['hora'][1]

                    pontoDeTrabalho.terceiro_ponto = f'{data} {hora}'
               
               if 'quarto_ponto' in dados:
                    novoPonto= {
                         "data":str(pontoDeTrabalho.quarto_ponto).split(' '),
                         "hora":str(dados['quarto_ponto']).split(' ')
                    }
                    data = novoPonto['data'][0]
                    hora = novoPonto['hora'][1]

                    pontoDeTrabalho.quarto_ponto = f'{data} {hora}'

               #atualizar o novo saldo do dia
               diaSeman = pontoDeTrabalho.dia_semana
               retornoSaldo = calDia(
                    pontoDeTrabalho.primeiro_ponto,
                    pontoDeTrabalho.segundo_ponto,
                    pontoDeTrabalho.terceiro_ponto,
                    pontoDeTrabalho.quarto_ponto,
                    (True if diaSeman == 'Sexta-Feira' else False)
               )  
               pontoDeTrabalho.saldo_dia = retornoSaldo.saldoDia()
               pontoDeTrabalho.save()#//

               response = {
                    'id':             pontoDeTrabalho.id,
                    'dia_semana':     pontoDeTrabalho.dia_semana,
                    'primeiro_ponto': pontoDeTrabalho.primeiro_ponto,
                    'segundo_ponto':  pontoDeTrabalho.segundo_ponto,
                    'terceiro_ponto': pontoDeTrabalho.terceiro_ponto,
                    'quarto_ponto':   pontoDeTrabalho.quarto_ponto,
                    'saldo_dia':      f'{str(pontoDeTrabalho.saldo_dia)}',
                    'registro':       pontoDeTrabalho.registro         
               }

          except TypeError:
               response = {
                    'status':'Error',
                    'mensagem':"Null"
               }
          

          return response

     #@auth.login_required
     def delete(self, registro):
          
          try:
               pontoDeTrabalho = Calendario.query.filter_by(registro=f'Registro-{registro}').first()
               registroPonto = pontoDeTrabalho.registro
               pontoDeTrabalho.delete()
               response = {
                    'status':'Ok',
                    'mensagem':f'O {registroPonto} foi deletado dos registros de ponto'
               }
          except AttributeError:
               response = {
                    'status':'Error',
                    'mensagem':'Informe um registro de pronto existente'
               }
          
          return response


class DirectCalendarioPass(Resource):

     def get(self):
          pontoDeTrabalho = Calendario.query.all()
          response = [{
               'id':             dados.id,
               'dia_semana':     dados.dia_semana,
               'primeiro_ponto': dados.primeiro_ponto,
               'segundo_ponto':  dados.segundo_ponto,
               'terceiro_ponto': dados.terceiro_ponto,
               'quarto_ponto':   dados.quarto_ponto,
               'saldo_dia':      f'{str(dados.saldo_dia)}',
               'registro':       dados.registro
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

               retornoSaldo = calDia(
                    dados['primeiro_ponto'],
                    dados['segundo_ponto'],
                    dados['terceiro_ponto'],
                    dados['quarto_ponto'],
                    (True if diaSeman.retornaDia() == 'Sexta-Feira' else False)
               )     
               
               pontoDeTrabalho = Calendario(dia_semana     = diaSeman.retornaDia(),
                                            primeiro_ponto = dados['primeiro_ponto'],
                                            segundo_ponto  = dados['segundo_ponto'],
                                            terceiro_ponto = dados['terceiro_ponto'],
                                            quarto_ponto   = dados['quarto_ponto'],
                                            saldo_dia      = retornoSaldo.saldoDia(),
                                            registro       = f'Registro-{registroUnico}'
               )

               pontoDeTrabalho.save()

               response = {
                   'id':              pontoDeTrabalho.id,
                    'dia_semana':     pontoDeTrabalho.dia_semana,
                    'primeiro_ponto': pontoDeTrabalho.primeiro_ponto,
                    'segundo_ponto':  pontoDeTrabalho.segundo_ponto,
                    'terceiro_ponto': pontoDeTrabalho.terceiro_ponto,
                    'quarto_ponto':   pontoDeTrabalho.quarto_ponto,
                    'saldo_dia':      f'{str(pontoDeTrabalho.saldo_dia)}',
                    'registro':       pontoDeTrabalho.registro
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
          
          except sqlalchemy.exc.IntegrityError:
               response = {
                    'status':'Error',
                    'mensagem':'Ponto já está registado no sistema!'
               }

          return response
