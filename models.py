from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///atividades.db', convert_unicode=True)  #Criando o banco atividades.db

db_session = scoped_session(sessionmaker(autocommit=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Pessoas(Base):
    __tablename__ = 'pessoas'  # a casse Pessoas criando a tabela pessoas
    id = Column(Integer, primary_key=True)  # campo da tabela
    nome = Column(String(40), index=True)   # campo da tabela
    idade = Column(Integer)                 # campo da tabela

class Atividades(Base):
    __tablename__ = 'atividades'    # a classe Atividades criando a tabela atividades
    id = Column(Integer, primary_key=True)     # campo da tabela
    nome = Column(String(80))                  # campo da tabela
    pessoa_id = Column(Integer, ForeignKey('pessoas.id'))    # campo chave extrangeira relacionando atividades com pessoas
    pessoa = relationship("Pessoas")

    def __repr__(self):
        return '<Atividades {}>' .format(self.nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Usuarios(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    senha = Column(String(20))

    def __repr__(self):
        return '<Usuario {}>'.format(self.login)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

def init_db():  # A função init_db cria o banco
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()   # Cria as tabelas do banco caso ainda não existam

