from datetime import datetime
from time import strftime


class CalculoDoDia():
     def __init__(self,ponto1, ponto2, ponto3, ponto4, menosUmaHora=False):
         self.pontos = {
              "ponto1":datetime.strptime(ponto1, "%Y-%m-%d %H:%M:%S"),
              "ponto2":datetime.strptime(ponto2, "%Y-%m-%d %H:%M:%S"),
              "ponto3":datetime.strptime(ponto3, "%Y-%m-%d %H:%M:%S"),
              "ponto4":datetime.strptime(ponto4, "%Y-%m-%d %H:%M:%S")
         }
         self.menosUmaHora = menosUmaHora
         
     def mecanismoDePonto(self):
          strFormat = '%H:%M:%S'

          tempoPadrao = {
               "primeiroTempo":"4:00:00",
               "segundoTempo" :'5:00:00' if self.menosUmaHora==False else '4:00:00'
          }

          horaPonto = {
               "ponto1":self.pontos['ponto1'].strftime(strFormat),
               "ponto2":self.pontos['ponto2'].strftime(strFormat),
               "ponto3":self.pontos['ponto3'].strftime(strFormat),
               "ponto4":self.pontos['ponto4'].strftime(strFormat)
          }

          calculoDeTempo = {
               "primeiroTempo":(
                    datetime.strptime(str(horaPonto['ponto2']), strFormat) - datetime.strptime(str(horaPonto['ponto1']), strFormat)
               ),
               "segundoTempo" :(
                    datetime.strptime(str(horaPonto['ponto4']), strFormat) - datetime.strptime(str(horaPonto['ponto3']), strFormat)
               )
          }

          calculoDeHora = {
               "primeiraHora":(
                    datetime.strptime(str(calculoDeTempo['primeiroTempo']), strFormat) - datetime.strptime(str(tempoPadrao['primeiroTempo']), strFormat)
               ),
               "segundoHora":(
                    datetime.strptime(str(calculoDeTempo['segundoTempo']), strFormat) - datetime.strptime(str(tempoPadrao['segundoTempo']), strFormat)
               )
          }

          saldoTotal = [
                    str(calculoDeHora['primeiraHora']),
                    str(calculoDeHora['segundoHora'])
          ]

          return saldoTotal
     
     def saldoDia(self):
          valoresDeTempo = {
                    "valor1":self.mecanismoDePonto()[0],
                    "valor2":self.mecanismoDePonto()[1]
          }

          primeiroTempo = str(valoresDeTempo['valor1']).split(':')
          segundoTempo  = str(valoresDeTempo['valor2']).split(':')

          extracaoDeMinutos = {
               "extracao1":(
                    (int(primeiroTempo[0]) * 60) +
                    (int(primeiroTempo[1])) +
                    (int(primeiroTempo[2]) / 100)
               ),
               "extracao2":(
                    (int(segundoTempo[0]) * 60) +
                    (int(segundoTempo[1])) +
                    (int(segundoTempo[2]) / 100)
               )
          }

          retornarValorTotal = extracaoDeMinutos["extracao1"] + extracaoDeMinutos["extracao2"]
          return retornarValorTotal
