# Importar o flask e sqlalchemy para o banco de dados
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
#Padrão para criação de qualquer site
app = Flask(__name__)

# Criar configuração do app e banco de dados, dentro do arquivo __init__
app.secret_key = 'aeecb39ba8c1e461f067730319f1cfa8'

if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
#Variável que pertence a clasee do Bcrypt que será usado para encriptografar senhas
bcrypt = Bcrypt(app)
#Criar variável para armazenar login
login_manager = LoginManager(app)
#Redireciona a página quando a pessoa tenta acessar uma tela que está com @login_required
login_manager.login_view = 'login'
#Remodelando a mensagem padrão para português
login_manager.login_message = 'Realize o login para acessar a página!'
#Mudando a cor da caixa com parâmetro 'alert-info' do bootstrap
login_manager.login_message_category = 'alert-info'

# Importar o arquivo de links 'routes' para poder rodar os links - IMPORTAR NO FINAL DO CÓDIGO, POIS O ROUTES PRECISA DO APP PARA FUNCIONAR
from comunidadeimpressionadora import routes
