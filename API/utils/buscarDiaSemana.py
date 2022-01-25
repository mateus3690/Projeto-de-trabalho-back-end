from pandas import Timestamp

class CalendariaSemanal():
    def __init__(self, data):
        self.data = data
    
    def retornaDia(self):
        temp = Timestamp(self.data) #'2022-01-01'
        dia  = temp.day_name()

        if dia == "Monday":
           dia = "Segunda-Feira"
        elif dia == "Tuesday":
            dia = "Terça-Feira"
        elif dia == "Wednesday":
            dia = "Quarta-Feira"
        elif dia == "Thursday":
            dia = "Quinta-Feira"
        elif dia == "Friday":
            dia = "Sexta-Feira"
        elif dia == "Saturday":
            dia = "Sábado"
        elif dia == "Sunday":
            dia = "Domingo"
        return dia

#uso
#v_dia = CalendariaSemanal('2022-01-27')
#pritn(v_dia.retornaDia())