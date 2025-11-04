🧠 Blogsite – Sistema Web com Flask

📋 Descrição

O Blogsite é uma aplicação web desenvolvida com Flask que permite o gerenciamento de usuários, postagens e redefinição de senha via e-mail.

O projeto foi implantado na Railway, com banco de dados SQLAlchemy e autenticação integrada pelo Flask-Login.

⚙️ Principais Tecnologias

Flask (framework web principal)

Flask-SQLAlchemy (ORM e conexão com banco)

Flask-Bcrypt (criptografia de senhas)

Flask-Login (autenticação e gerenciamento de sessão)

Flask-Mail / SendGrid API (envio de e-mails)

Gunicorn (servidor WSGI para deploy)

Railway (hospedagem e deploy contínuo)


🧩 Funcionalidades Principais

Cadastro e login de usuários

Criação, edição e exclusão de posts

Sistema de redefinição de senha com token seguro

Envio de e-mails via SendGrid API

Banco de dados persistente com SQLAlchemy

Interface responsiva baseada em Bootstrap


🚀 Deploy na Railway

Configurações Flask

SECRET_KEY=chave_secreta

DATABASE_URL=sqlite:///comunidade.db  # ou URL do banco Railway

Configurações de E-mail (SendGrid)

SENDGRID_API_KEY=SG.xxxxxxx

MAIL_DEFAULT_SENDER=seuemailverificado@dominio.com

MAIL_PASSWORD=suasenhaappgmail

MAIL_PORT=587

MAIL_SERVER=smtp.gmail.com

MAIL_USE_TLS=True


✉️ Reset de Senha (SendGrid)

O fluxo de redefinição de senha envia um link com token temporário ao e-mail do usuário.

Para que o envio funcione corretamente:

Configure uma API Key válida no SendGrid.

Verifique o remetente em Sender Authentication.

Atualize o MAIL_DEFAULT_SENDER com o e-mail verificado.


🛠️ Estrutura Básica do Projeto

blogsite/

│

├── __init__.py          # Configurações do app e extensões

├── models.py            # Modelos e tabelas do banco

├── routes.py            # Rotas principais e lógicas de negócio

├── static/              # Arquivos CSS, JS e imagens

├── templates/           # Páginas HTML (login, home, etc.)

└── forms.py             # Formulários WTForms


👨‍💻 Autor
Projeto desenvolvido por Bruno Ken.
