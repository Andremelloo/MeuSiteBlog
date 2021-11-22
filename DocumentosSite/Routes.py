from flask import render_template, request, flash, redirect, url_for, abort
from DocumentosSite import app, database, bcrypt
from DocumentosSite.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from DocumentosSite.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

# login_required é para bloquer as paginas que voce quer, quando a pessoa não esta com o login feito no site ainda.
#current_user verifica qual usuario esta na pagina, esta logado ou nao esta logado... usando o current_user.is_authenticated
# current_user é a pessoa que esta logado na pagina, se precisar pegar informacao dela usa exemplo current_user.username



@app.route("/")  ## a cada funçao é uma pagina do site.
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)

@app.route("/contato")  ## a cada funçao é uma pagina do site.
def contato():
    return render_template('contato.html')

@app.route("/usuarios")  ## a cada funçao é uma pagina do site.
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all() ### Todos os usuario no banco de dados.
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route("/login_conta",methods=['GET', 'POST'])  ## a cada funçao é uma pagina do site.
def login_conta():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, form_login.password.data): ## se usuario existe e a senha é a mesma do banco de dados entao:
            login_user(usuario, remember=form_login.lembrar_dados.data) ## fazer o login e relembrar o lembrar dados no site. True ou false
            flash('Login feito com sucesso no e-mail: {}'.format(form_login.email.data), 'alert-success')
            parametro_next = request.args.get('next') ## procura o 'next 'na pagina
            if parametro_next:
                return redirect(parametro_next) ## vai retirecionar para a pagina que ele estava acessando, depois que fazer o login
            else:

                ## retireciona para a pagina 'home' inicio
                return redirect(url_for('home'))
        else:
            flash('Falha no login. Email ou senha incorretos', 'alert-danger')




    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.password.data)
        #criar usuario
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data,password=senha_cript)
        #adicionar a sessao
        database.session.add(usuario)
        # comit na sessao
        database.session.commit()

        flash('Conta criada para o e-mail: {}'.format(form_criarconta.email.data), 'alert-success')
        ##  exibir criou conta com sucesso obs: tem que deixar assiim se o form estiver dois botoes iguais
        return redirect(url_for('home'))
    return render_template('login_conta.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route('/sair')
@login_required # login_required é para bloquer as paginas que voce quer, quando a pessoa não esta com o login feito no site ainda.
def sair():
    logout_user()
    flash(f'Logout feito com sucesso', 'alert-success')
    return redirect(url_for('contato'))

@app.route('/perfil')
@login_required # login_required é para bloquer as paginas que voce quer, quando a pessoa não esta com o login feito no site ainda.
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil)) ##foto\-perfil = url_for('static', filename='fotos_perfil/nome_arquivo.extensao') format, ele usa a variavel foto_perfil do Models.
    return render_template('perfil.html', foto_perfil=foto_perfil) ## passando a vareavel para o html, para poder usar

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form_criar_post = FormCriarPost()  ### import a class criar post do Models
    if form_criar_post.validate_on_submit(): ## colocando o post no banco de dados
        post = Post(titulo=form_criar_post.titulo.data, corpo=form_criar_post.corpo.data, autor=current_user)  ## import o Post do Models ( passando os parametros pra ele.)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com succeso', 'alert-success') ## enviando uma msg para o usuario. 'alert-success' é a class do botstrap
        return redirect(url_for('home'))

    return render_template('criarpost.html', form_criar_post=form_criar_post)  #### passa o parametro form_criar_post para ele pode ir para o HTML


## import secrets
## import os
## from PIL import Image

def salvar_imagem(imagem):
    # adicionar um codigo aleatorio no nome da imagem, para nao ter repetida.
    codigo = secrets.token_hex(8) ## colocar um codigo de 8 numeros
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    # reduzier o tamanho da imagem, para ter mais espaço
    tamanho = (200,200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # salvar a imagem na pasta fotos_perfil
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo
    # mudar  o campo foto_perfil do usuario para o novo nome da imagem


def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            ## adicionar o campo.label( excel ) na lista de cursos
            if campo.data: ## se o campo dos cursos em boleano esta marcado.
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)




@app.route('/perfil/editar',methods=['GET', 'POST']) ### methods=['GET', 'POST']) é autorizaar o metodo POSTAR algo no site, enviar algo para o site.
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():  ## validar o validate do model
        current_user.email = form.email.data # subistituir o email do usuario para qual ele escreveu
        current_user.username = form.username.data ## subistituir o nome do usuario para qual ele escreveu
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem

        
        current_user.cursos = atualizar_cursos(form)

        database.session.commit()  ##o banco de dados que ja esta adicionado no banco de dados, entao so da um commit igual um uptade.
        flash('Perfil atualizado com succeso')
        return redirect(url_for('perfil')) ## depois retiriciona para a pagina perfil

    elif request.method == "GET":  ## verifica se o usuario esta carregando a pagina se sim.. executa ..deixar o seu formulario preechido ja, tenho que da um modo GET no meu site
        form.username.data = current_user.username
        form.email.data = current_user.email

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editar_perfil.html', foto_perfil=foto_perfil, form=form) ## aqui voce passa as variavel para o HTML

@app.route('/post/<post_id>', methods=['GET', 'POST'])  ## <post_id> é uma variavel chamada com esse nome, pra ir mudando conferme os post que for clicando dos usuario
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id) ### pegando informacao do banco de dados
    if current_user == post.autor:  ## se o usuario atual for o mesmo que fez o post, execute.
        form_editar_post = FormCriarPost() ## estou usando a class do FormCriarPost para realizar a edicao do post, eu poderia fazer outra class no 'forms' se fosse o caso.

        ##  ja deixar o textos preenchidos
        if request.method == 'GET':
            form_editar_post.titulo.data = post.titulo
            form_editar_post.corpo.data = post.corpo

        ###  substituido o que foi excrito para o atual
        elif form_editar_post.validate_on_submit():
            post.titulo = form_editar_post.titulo.data ## o que estava ecrito e o que eta escrito atual
            post.corpo = form_editar_post.corpo.data
            database.session.commit()  ## adicionando no banco de dados
            flash('Post atualizado com sucesso!!','alert-success')  ## enviando uma msg para o usuario. 'alert-success' é a class do botstrap
            return redirect(url_for('home'))  ## retirecionar para a pagina home




    else:
        form_editar_post = None



    return render_template('post.html', post=post, form_editar_post=form_editar_post)  ## passando as informacoes para o HTML



@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])  ## <post_id> é uma variavel chamada com esse nome, pra ir mudando conferme os post que for clicando dos usuario
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id) ### pegando informacao do banco de dados
    if current_user == post.autor: ## se o usuario atual for o mesmo que fez o post, execute.
        database.session.delete(post)
        database.session.commit()
        flash('Seu Post foi excluido com succeso','alert-success')
        return redirect(url_for('home'))

    else:
        abort(403) ### caso o usuario tente excluir usando somente o URL digitando http://127.0.0.1:5000/post/1/ exluir