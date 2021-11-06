from flask import Flask, render_template, url_for, request, flash, redirect
from  forms import FormLogin, FormCriarConta

app = Flask(__name__)

lista_usuarios = ['joao','andre','Cecilia']


app.config['SECRET_KEY'] = '362bac6fa602b430ed21c6ec0293c626'

@app.route("/")  ## a cada funçao é uma pagina do site.
def inicio():
    return render_template('home.html')

@app.route("/contato")  ## a cada funçao é uma pagina do site.
def contato():
    return render_template('contato.html')

@app.route("/usuarios")  ## a cada funçao é uma pagina do site.
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route("/login_conta",methods=['GET', 'POST'])  ## a cada funçao é uma pagina do site.
def login_conta():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        flash('Login feito com sucesso no e-mail: {}'.format(form_login.email.data), 'alert-success')
        ## exibir fez login com sucesso
        return redirect(url_for('inicio'))

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        flash('Conta criada para o e-mail: {}'.format(form_criarconta.email.data), 'alert-success')
        ##  exibir criou conta com sucesso obs: tem que deixar assiim se o form estiver dois botoes iguais
        return redirect(url_for('inicio'))
    return render_template('login_conta.html', form_login = form_login, form_criarconta= form_criarconta)

if __name__== '__main__':
    app.run(debug=True) # debug, faz atualizar automatico, sem precisar parar e dar RUN novamente