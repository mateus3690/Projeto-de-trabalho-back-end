import repackage
repackage.up()

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, NUMERIC
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from utils.verificarDB import DBexiste

base = 'BaseLocal'
engine = create_engine(f'sqlite:///{base}.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Calendario(Base):
    
     __tablename__ = 'tb_calendario'
     id = Column(Integer, primary_key=True, unique=True)
     dia_semana     = Column(String(30))
     primeiro_ponto = Column(String(30))
     segundo_ponto  = Column(String(30))
     terceiro_ponto = Column(String(30))
     quarto_ponto   = Column(String(30))
     saldo_dia      = Column(NUMERIC(5,2))
     registro       = Column(String(30), unique=True)
     chave          = Column(String(11))

     def __repr__(self):
         return f'<dia {self.chave}>'
     
     def save(self):
          db_session.add(self)
          db_session.commit()
     
     def delete(self):
          db_session.delete(self)
          db_session.commit()

class FechamentoDoMes(Base):
    
     __tablename__ = 'tb_fechamento'
     id          = Column(Integer, primary_key=True, unique=True)
     mes         = Column(String(30))
     saldo_extra = Column(NUMERIC(5,2))
     valor_extra = Column(NUMERIC(5,2))
     saldo_dia   = Column(NUMERIC(5,2))
     chave       = Column(String(40))

     def __repr__(self):
         return f'<dia {self.chave}>'
     
     def save(self):
          db_session.add(self)
          db_session.commit()
     
     def delete(self):
          db_session.delete(self)
          db_session.commit()



class Usuario(Base):
     
     __tablename__ = 'tb_usuario'
     id = Column(Integer, primary_key=True)
     login = Column(String(16), unique=True)
     senha = Column(String(16))
     tipo_usuario = Column(String(1), default='N')# N - normal | A - administrador


     def __repr__(self):
         return f'<Usuario {self.usuario}>'
     
     def save(self):
          db_session.add(self)
          db_session.commit()
     
     def delete(self):
          db_session.delete(self)
          db_session.commit()

class Login(Base):

     __tablename__ = 'tb_login'
     id = Column(Integer, primary_key=True)
     nome = Column(String(16))
     nascimento = Column(String(10))
     cpf = Column(String(11), index=True, unique=True)
     email = Column(String(30), index=True, unique=True)
     senha = Column(String(50))

     def __repr__(self):
         return f'<Login {self.nome}>'
     
     def save(self):
          db_session.add(self)
          db_session.commit()
     
     def delete(self):
          db_session.delete(self)
          db_session.commit()


def init_db():
     Base.metadata.create_all(bind=engine)

#if DBexiste(base) == False:
init_db()
