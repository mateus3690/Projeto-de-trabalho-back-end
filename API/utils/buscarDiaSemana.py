from pandas import Timestamp

class CalendariaSemanal():
    def __init__(self, data):
        self.data = data
    
    def retornaDia(self):
        temp = Timestamp(self.data) #'2022-01-01'        
        dia = {
                "Monday"   :"Segunda-Feira",
                "Tuesday"  :"Terça-Feira" ,
                "Wednesday":"Quarta-Feira" ,      
                "Thursday" :"Quinta-Feira" ,      
                "Friday"   :"Sexta-Feira" ,      
                "Saturday" :"Sábado"    ,      
                "Sunday"   :"Domingo"    
        }    
        return dia[temp.day_name()]
