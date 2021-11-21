from DocumentosSite import database, login_manager ## importar meu banco de dados
from datetime import datetime
from flask_login import UserMixin

#UserMixin para manter o login do seu usuario quando sair do site etc, precisa colocar na classe usuario..
#login_manager voce faz a funçao para carregar o usuario e pegar pelo id dele


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario)) ## encontrar usuario com o id dele



class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True) ## primery_key ele identifica que usuario é unico.
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='Default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True, passive_deletes=True)
    cursos = database.Column(database.String, nullable=False, default= 'Nao Informado')


    def contar_posts(self):
        return len(self.posts)



class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False ) ## usuario.id é da class usuario.

