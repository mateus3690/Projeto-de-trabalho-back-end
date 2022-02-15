import psycopg2
import repackage
repackage.up()

def conexao():
    try:
        conn = psycopg2.connect(database ="", 
                                user = "", 
                                password = "", 
                                host = "", 
                                port ="")
    
        cur = conn.cursor()

    except (Exception, psycopg2.DatabaseError) as error:    
        print ("Error na conexão", error)
       
    return conn, cur