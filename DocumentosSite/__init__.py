from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)


app.config['SECRET_KEY'] = '362bac6fa602b430ed21c6ec0293c626'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meusite.db' ## criando banco de dados no mesmo local do programa

database = SQLAlchemy(app) ## banco de dados
bcrypt = Bcrypt(app) ## criptografia de senha
login_manager = LoginManager(app)
login_manager.login_view = 'login_conta'  ## se alguem entrar no site tentando acessar uma pagina que so entra com login, ele ja vai direcionar para essa pagina login_conta
login_manager.login_message = 'faça o login'
login_manager.login_message_category = 'alert-info'  # pega no site do bugstrap

from DocumentosSite import Routes