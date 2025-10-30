from wsgiref.validate import validator

from flask_wtf import FlaskForm
#Importar FileField (campo de carregar arquivos) e FileAllowed (verifica extensões de arquivo)
from flask_wtf.file import FileField, FileAllowed
#importar forms de cada campo (string, senha, envio (botão, texto grande)
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
#importar validadores de campos (dado obrigatório, tamanho, email, igual à,
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
#Importar usuário para poder fazer validação de email
from blogsite.models import Usuario
#Importar da biblioteca de flask_login LoginManager para facilitar o login do site e current_user, para pegar infos em tempo real do usuário
from flask_login import LoginManager, current_user



class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao = PasswordField('Confirme sua senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criar_conta = SubmitField('Criar conta')

    #Um dos métodos da classe FalskForm roda qualquer função que tenha o 'validate_'
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first() #Inserir o .data para puxar a informação do formulário
        if usuario:
            raise ValidationError('Email já cadastrado! Cadastre-se com um outro e-mail ou faça login para continuar')

"""Para realizar o login para o site devemos instalar a biblioteca pip install flask-login"""
class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer login')

"""Nova classe para criar formulário em página de editar perfil"""
class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    #Adicionar os cursos para poder indicar quais deles o usuário realiza
    curso_excel = BooleanField('Excel Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_ppt = BooleanField('Apresentações Impressionadoras')
    curso_sql = BooleanField('SQL Impressionador')
    botao_submit_editar_perfil = SubmitField('Confirmar edição')

    # Um dos métodos da classe FalskForm roda qualquer função que tenha o 'validate_'
    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()  # Inserir o .data para puxar a informação do formulário
            if usuario:
                raise ValidationError('Já existe um usuário com esse e-mail. Cadastre um outro e-mail')


class FormCriarPost(FlaskForm):
    titulo = StringField('Título do post', validators=[DataRequired(), Length(2,140)])
    corpo = TextAreaField('Escreva seu post aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post!')
    botao_submit_editar = SubmitField('Editar Post!')


class PedirResetForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    botao_submit = SubmitField('Solicitar Redefinição de Senha')

    #Um dos métodos da classe FalskForm roda qualquer função que tenha o 'validate_'
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first() #Inserir o data para puxar a informação do formulário
        if usuario is None:
            raise ValidationError('Não existe nenhum registro para o e-mail mencionado. Registre-se primeiro!')


class ResetSenhaForm(FlaskForm):
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao = PasswordField('Confirme sua senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit = SubmitField('Confirmar Redefinição de Senha')