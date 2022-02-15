# import os
# x = os.getenv('HOST')
# print(x)

# y = ["%s","%s","%s","%s","%s","%s","%s"]

# print(len(y))

# import psycopg2
  
# def connect():
  
#     try:
  
#         conn = psycopg2.connect(database ="ywmmjubu", 
#                             user = "ywmmjubu", 
#                             password = "i28AT2BHR5Z7no5IBXkXnZfeUSU7-pKv", 
#                             host = "kesavan.db.elephantsql.com", 
#                             port ="5432")
  
#         cur = conn.cursor()

#     except (Exception, psycopg2.DatabaseError) as error:
          
#         print ("Error ", error)
       
#     return conn, cur
  
# def create_table():
  
    
#      conn, cur = connect()
 
#      try:
#          cur.execute('CREATE TABLE emp (id INT PRIMARY KEY, name VARCHAR(10), salary INT, dept INT)')       
#      except:
 
#          print('error')
 
#      conn.commit() 
 
  
# def insert_data(id = 1, name = '', salary = 1000, dept = 1):
 
#      conn, cur = connect()
 
#      try:
       
#          cur.execute('INSERT INTO emp VALUES(%s, %s, %s, %s)',
#                                      (id, name, salary, dept))
     
#      except Exception as e:
 
#          print('error', e)
   
#      conn.commit()
  
  
# def fetch_data():
  
#     conn, cur = connect()
  
    
#     try:
#         cur.execute('SELECT * FROM emp where id = 1')
      
#     except:
#         print('error !')
  
    
#     data = cur.fetchall()
  
#     print(data)
#     return data
  
# def print_data(data):
  
#     print('Query result: ')
    
  
    
#     for row in data:
#         print('id: ', row[0])
#         print('name: ', row[1])
#         print('salary: ', row[2])
#         print('dept: ', row[3])
#         print('----------------------------------')
        
       
# def delete_table():
  
#     conn, cur = connect()
  
    
#     try:
  
#         cur.execute('DROP TABLE emp')

#     except Exception as e:
#         print('error', e)

#     conn.commit()
  
  
# if __name__ == '__main__':
  
    
  
#     create_table()
  
    
#     insert_data(1, 'adith', 1000, 2)
#     insert_data(2, 'tyrion', 100000, 2)
#     insert_data(3, 'jon', 100, 3)
#     insert_data(4, 'daenerys', 10000, 4)
  
    
#     data = fetch_data()
  
#     print_data(data)
  
    
    
    
    #delete_table()

#from numpy import insert
import repackage
repackage.up()

from config.dbase import ComponenteDB

# consulta = ComponenteDB(nomeTabela='emp', condicoesDeConsulta='id=5')

# print(consulta.consultarDados())
# pontoDeTrabalho = ComponenteDB(nomeTabela='tb_calendario', 
#                                valorColunaAtualizar={'w':'t'}
#                             , condicoesDeConsulta='x = 1232')
# pontoDeTrabalho = pontoDeTrabalho.atualizarDados()

# x = {
# 	'dia_semana':     f"1",
# 	'primeiro_ponto': f"2"
# }

# x['teste'] = 'teste'
# print(x)


# response = [{
#             'id':             dados[0],
#             'id_usuario':     dados[1],
#             'dia_semana':     dados[2],
#             'primeiro_ponto': str(dados[3]),
#             'segundo_ponto':  str(dados[4]),
#             'terceiro_ponto': str(dados[5]),
#             'quarto_ponto':   str(dados[6]),
#             'saldo_dia':      str(dados[7]),
#             'registro':       dados[8],
#             'chave'   :       dados[9]
#             } for dados in pontoDeTrabalho]

# print(response)
# condicao = f"chave='12345667' and registro='123teste'"
# teste = ComponenteDB(nomeTabela='tb_calendario',
#                     valorConsulta="dia_semana",
#                     condicoesDeConsulta=condicao)



# inserir = ComponenteDB(nomeTabela='emp',inserirColunas='5,mateus,2000,69', salvar=True)
# inserir.inserirDados()
#print(consulta.consultarDados())

condicao = f"email='mateusmag3690@gmail.com' and senha='7c2197865cda17f7846fd3101143e7b2'"

usuario = ComponenteDB(nomeTabela='tb_usuario', condicoesDeConsulta=condicao)
usuario = usuario.consultarDados()

response = [{
    'id':         dados[0],
    'nome':       dados[1],
    'nascimento': dados[2],
    'cpf':        dados[3],
    'email':      dados[4]
} for dados in usuario]

print(response)