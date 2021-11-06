from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import  DataRequired, Length, Email, EqualTo

## StringField
## PasswordField  uma senha
## SubmitField  um botão
## BooleanField  lembrar do login ou nao

## DataRquired Campo obrigatorio
## Length - tamanho dos caracteres exemplo de 6 a 20 - tamanho da senha
## Email Validacao de email
## EqualTo - o campo tem que ser igual ao outro

#### preenchimento de formulario
class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuario', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Criar senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao = PasswordField('Confirmacao da senha', validators=[DataRequired(), EqualTo('password')])
    botao_submit_criarconta = SubmitField('Criar Conta')

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer login')

