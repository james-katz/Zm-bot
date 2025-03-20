from peewee import *
from datetime import datetime


# Configuração do banco de dados
db = SqliteDatabase ("banco.sqlite3")

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id =  TextField()
        
class Interacao(BaseModel):
    id = AutoField()  
    user_id = ForeignKeyField(User, backref='interacoes')

class Premiacao(BaseModel):
    id = AutoField()
    data_premiacao = DateTimeField(default=datetime.now)
    user_id = ForeignKeyField(User, backref='awards')

db.create_tables([User, Interacao, Premiacao])