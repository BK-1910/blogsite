from comunidadeimpressionadora import database, login_manager
from datetime import datetime
#UserMixin é um parâmetro a ser passado para nossa classe e já atribui todas as características que o login_manager precisa pra poder controlar o login
from flask_login import UserMixin

#Decorator necessário para que o programa entenda que a função load_usuario deve ser carregada em login_manager
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

"""Parâmetros de .Column():
    - primary_key -> indica que é uma chave única
    - unique -> indica que aquele campo não pode se repetir
    - nullable -> indica se tal campo pode ser único ou não
    - default -> indica qual é o objeto inicial
    
    Parâmetros de .relationship():
    - lazy -> indica se tal variável herda todas as características
    - backref -> cria uma referência reversa automática entre as tabelas
    
    Métodos de database:
    - .relationship() -> cria relacionamento entre as classes/ subclasses para inserir ou trocar informações
    - .Column() -> cria uma coluna no database indicando qual nome do campo bem como suas características
        - .DateTime -> cria coluna de data
        - .Integer -> cria coluna de números inteiros
        - .String -> cria coluna de texto comum
        - .Text -> cria coluna de textos grandes
    - .ForeignKey -> indica que tal coluna usará uma chave de outra tabela do banco de dados (DEVE SER O SEGUNDO PARÂMETRO DE .Column() E A CLASSE UTILIZADA DEVE ESTAR EM MINÚSCULO)
        
"""
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)
    cursos = database.Column(database.String, nullable=False, default='Não Informado')

    #Criar métdodo exclusivo para contar posts de cada usuário
    def contar_posts(self):
        return len(self.posts)

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
