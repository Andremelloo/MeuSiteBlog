from flask import Flask, render_template, url_for

app = Flask(__name__)

lista_usuarios = ['joao','andre','Cecilia']


@app.route("/")  ## a cada funçao é uma pagina do site.
def inicio():
    return render_template('home.html')

@app.route("/contato")  ## a cada funçao é uma pagina do site.
def contato():
    return render_template('contato.html')

@app.route("/usuarios")  ## a cada funçao é uma pagina do site.
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)



if __name__== '__main__':
    app.run(debug=True) # debug, faz atualizar automatico, sem precisar parar e dar RUN novamente