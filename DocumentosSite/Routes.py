from flask import render_template, request, flash, redirect, url_for
from DocumentosSite import app, database, bcrypt
from DocumentosSite.forms import FormLogin, FormCriarConta, FormEditarPerfil
from DocumentosSite.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required


# login_required é para bloquer as paginas que voce quer, quando a pessoa não esta com o login feito no site ainda.
#current_user verifica qual usuario esta na pagina, esta logado ou nao esta logado... usando o current_user.is_authenticated
# current_user é a pessoa que esta logado na pagina, se precisar pegar informacao dela usa exemplo current_user.username

lista_usuarios = ['joao','andre','Cecilia']

@app.route("/")  ## a cada funçao é uma pagina do site.
def home():
    return render_template('home.html')

@app.route("/contato")  ## a cada funçao é uma pagina do site.
def contato():
    return render_template('contato.html')

@app.route("/usuarios")  ## a cada funçao é uma pagina do site.
@login_required
def usuarios():
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
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required # login_required é para bloquer as paginas que voce quer, quando a pessoa não esta com o login feito no site ainda.
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil)) ##foto\-perfil = url_for('static', filename='fotos_perfil/nome_arquivo.extensao') format, ele usa a variavel foto_perfil do Models.
    return render_template('perfil.html', foto_perfil=foto_perfil) ## passando a vareavel para o html, para poder usar

@app.route('/post/criar')
@login_required
def criar_post():
    return render_template('criarpost.html')

@app.route('/perfil/editar',methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():  ## validar o validate do model
        current_user.email = form.email.data # subistituir o email do usuario para qual ele escreveu
        current_user.username = form.username.data ## subistituir o nome do usuario para qual ele escreveu
        database.session.commit()  ##o banco de dados que ja esta adicionado no banco de dados, entao so da um commit igual um uptade.
        flash('Perfil atualizado com succeso')
        return  redirect(url_for('perfil')) ## depois retiriciona para a pagina perfil

    elif request.method == "GET":  ## verifica se o usuario esta carregando a pagina se sim.. executa ..deixar o seu formulario preechido ja, tenho que da um modo GET no meu site
        form.username.data = current_user.username
        form.email.data = current_user.email

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editar_perfil.html', foto_perfil=foto_perfil, form=form) ## aqui voce passa as variavel para o HTML