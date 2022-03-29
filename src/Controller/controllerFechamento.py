import repackage
repackage.up()

from database.dbase import ComponenteDB
from utils.calcularHoras import CalculoDoDia as calDia , ManipulacaoDeTempo, ManipulacaoSalario
from utils.buscarDiaSemana import CalendariaSemanal
#from config.auth import AuthSystem
from flask_restful import Resource


class DirectFechamento(Resource):
     
     def get(self, chave, mes):
          
          try: 
               mes = str(mes[0:7]).replace('-','')
               condicao = f"chave='{chave}' and mes_ano = '{mes}' order by 1 desc"
              
               #calendario
               pontoDeTrabalho = ComponenteDB(nomeTabela='tb_calendario', condicoesDeConsulta=condicao)
               pontoDeTrabalho = pontoDeTrabalho.consultarDados()

               #usuario
               pessoa = ComponenteDB(nomeTabela='tb_usuario', condicoesDeConsulta=f"cpf='{chave}'")
               pessoa = pessoa.consultarDados()
               
               dadosPessoa = {
                    'nome' : pessoa[0][1],
                    'email': pessoa[0][4],
                    'salario': pessoa[0][6]
               }
               
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
               
               valorContabel = {
                    "salarioTotal": 0,
                    "valorExtra": 0
               }
               saldo = 0
               salarioExtra = 0

               for valor in response:
                    saldo += float(valor['saldo_dia']) 

               hora = ManipulacaoDeTempo(tempo=saldo)
               if len(response) >= 27:
                    salarioExtra = ManipulacaoSalario(float(dadosPessoa['salario']), float(hora.minutoHora()[1]))
                    salarioExtra = salarioExtra.valorExtra()  
                    valorContabel['valorExtra']   = salarioExtra
               valorContabel['salarioTotal'] = (float(dadosPessoa['salario']) + valorContabel['valorExtra'] ) 

               responseFormat = {
                    "data":response[0]['primeiro_ponto'][0:7],
                    "TotalMinutoExtra": f'{int(saldo)}min',
                    "horasExtra": hora.minutoHora()[0],
                    "contidadeDia":f'{len(response)} dia(s)',
                    "usuario":dadosPessoa['nome'],
                    "email":dadosPessoa['email'],
                    "valorOriginal": f"{float(dadosPessoa['salario'])}",
                    "valorExtra": f"{valorContabel['valorExtra']:.2f}",
                    "valorTotal": f"{valorContabel['salarioTotal']:.2f}"
               }

               if response == []:
                    response = {"mensagem":"Nenhum registro de ponto no momento"}

          except (AttributeError, IndexError, UnboundLocalError):
               response = {
                    'status':'Error',
                    'mensagem':f"Ponto de trabalho, não existe nos registros"
               }  

          return responseFormat 
     
     

