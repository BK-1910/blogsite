import os
from dotenv import load_dotenv
import sqlalchemy
# Importar o flask e sqlalchemy para o banco de dados
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message

# Carrega as variáveis do arquivo .env
load_dotenv()

#Padrão para criação de qualquer site
app = Flask(__name__)

# Criar configuração do app e banco de dados, dentro do arquivo __init__
app.secret_key = os.environ.get('SECRET_KEY')

# Configurações do banco
if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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


#Criar configurações para poder utilizar gmail no projeto (enviar links/ mensagens/ etc)
#Teste local
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'teste@gmail.com'
# app.config['MAIL_PASSWORD'] = 'sua senha'

#Configuração para envio real (usando railway)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'False') == 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])

mail = Mail(app)

#Importar models, pois lá está a configuração do banco de dados
from blogsite import models
#Criar engine para criar banco de dados caso não exista
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
#Verificar se dentro da engine existe a tabela usuários
inspector = sqlalchemy.inspect(engine)
#No inspector não inserir nome do banco sempre em minúsculo
if not os.path.exists('instance/comunidade.db'):
    with app.app_context():
        database.create_all()
        print("Tabelas faltantes criadas - 1")
elif not inspector.has_table("usuario"):
    with app.app_context():
        # ✅ APENAS cria a tabela específica que está faltando
        database.create_all()
        print("Tabelas faltantes criadas - 2")
else:
    print("Base de dados já existente!")

# Importar o arquivo de links 'routes' para poder rodar os links - IMPORTAR NO FINAL DO CÓDIGO, POIS O ROUTES PRECISA DO APP PARA FUNCIONAR

from blogsite import routes
