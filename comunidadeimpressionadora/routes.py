from fileinput import filename
from flask import render_template, redirect, url_for, flash, request, abort
from comunidadeimpressionadora import app, database, bcrypt
#Importar formulário para uso em templates/ páginas
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora.models import Usuario, Post
#login_user armazena informação de qual o usuário logado, logout_user -> realiza logout, current_user -> verifica usuário da página no momento
from flask_login import login_user, logout_user, current_user, login_required
#Importar a biblioteca secrets para alteração de nome de imagens uplodadas
import secrets
#Importar os para poder tratar caminhos no projeto
import os
#Instalar pip install Pillow para tratar tamanho de imagens
from PIL import Image


# Criar primeiro link para poder por o site no ar
@app.route("/")
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        #Verificar se usuário existe e se a senha inputada corresponde ao usuário
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            #Criar metodo para poder de fato logar o usuário
            login_user(usuario, remember=form_login.lembrar_dados.data)
            #Exibir mensagem de login realizado
            flash(f'Login realizado no e-mail: {form_login.email.data}!', 'alert-success')
            #Criar uma parâmetro para se caso exista o parâmetro next na url o site redireciona para a página que o usuário tentou logar antes
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                #Redirecionar para homepage
                return redirect(url_for('home'))
        else:
            #Exibir mensagem de login NÃO realizado
            flash(f'Falha no login! E-mail: {form_login.email.data} ou senha incorretos', 'alert-danger')
    if form_criar_conta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        #Encriptografar senha antes da criação do usuário utilizando o bcrypt
        senha_crypt = bcrypt.generate_password_hash(form_criar_conta.senha.data)
        #Criar o usuário
        usuario = Usuario(username=form_criar_conta.username.data , email=form_criar_conta.email.data, senha=senha_crypt)
        with app.app_context():
            database.session.add(usuario) #Adicionar a sessão
            database.session.commit() #Commit na sessão
        #Exibir mensagem de conta criada
        flash(f'Conta criada com sucesso para e-mail: {form_criar_conta.email.data}', 'alert-success')
        #Redirecionar para homepage
        return redirect(url_for('home'))

    return render_template('login.html',form_login = form_login, form_criar_conta = form_criar_conta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    # Exibir mensagem de logout
    flash(f'Logout feito com sucesso!', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    #Para poder usar a foto atrelada ao perfil, devemos colocar o diretório da pasta de fotos 'static' e definir o parâmetro fiolename com current_user.foto_perfil
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo =form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash(f'Post criado com sucesso!', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)

#Função para tratar imagem carregada
def salvar_imagem(imagem):
    # Adicionar um código aleatório no nome da imagem
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    #Definir caminho a ser salvo a imagem
    caminho_completo = os.path.join(app.root_path, 'static\\fotos_perfil', nome_arquivo)
    # Reduzir o tamanho da imagem
    tamanho = (220, 220)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # Salvar a imagem na pasta fotos_perfil
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


#Função que atualiza cursos do usuário
def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            #Verificar se o campo foi marcado na caixa de seleção
            if campo.data:
                #Adicionar o texto de campo.label na lista de cursos OBS: .text armazena somente o texto
                lista_cursos.append(campo.label.text)

    return ';'.join(lista_cursos)


#Metodo aplicado deve conter ['GET', 'POST'] para poder funcionar butões
@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        #Adicionar a nova foto adicionada
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            # Mudar o campo de foto_perfil com nova foto enviada
            current_user.foto_perfil = nome_imagem
        #Adicionar os cursos selecionados
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash('Perfil atualizado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        pass
    # Para poder usar a foto atrelada ao perfil, devemos colocar o diretório da pasta de fotos 'static' e definir o parâmetro fiolename com current_user.foto_perfil
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    #post_id servirá para exibir post clicado
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        #Lógica para editar post
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post Atualizado com sucesso!', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)

@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    #post_id servirá para vincular qual post será excluído
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluído com sucesso!', 'alert-warning')
        return redirect(url_for('home'))
    else:
        #abort é usado para indicar que tal usuário não tem permissão de realizar tal ação
        abort(403)