from flask_wtf import FlaskForm
from flask_wtf.file import  FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from DocumentosSite.models import Usuario
from flask_login import current_user


## FileField é para escolher a foto no seu computador e FileAllowed é um valitador de arquivos
## StringField
## PasswordField  uma senha
## SubmitField  um botão
## BooleanField  lembrar do login ou nao

## DataRquired Campo obrigatorio
## Length - tamanho dos caracteres exemplo de 6 a 20 - tamanho da senha
## Email Validacao de email
## EqualTo - o campo tem que ser igual ao outro
## validators=[DataRequired()] é pra deixar o campo obrigatorio



#### preenchimento de formulario
class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuario', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Criar senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao = PasswordField('Confirmacao da senha', validators=[DataRequired(), EqualTo('password')])
    botao_submit_criarconta = SubmitField('Criar Conta')


    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail ja cadastrado')

## Tem que colocar validate_ para o .validate_on_submit() verificar essa funcao.





class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de usuario', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg','png'])])

    curso_python = BooleanField('Python')
    curso_excel = BooleanField('Excel')
    curso_vba = BooleanField('VBA')
    curso_powerbi = BooleanField('PowerBI')

    botao_submit_editarperfil = SubmitField('Confirmar Edição')


    def validate_email(self, email):
        # verificar se o cara mudou de email
        if current_user.email != email.data:  ## Se o email do usuario for diferente do email que ele escrever
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:  ## se houver um email no banco de dados, vou enviar uma msg de erro
                raise ValidationError('Ja existe um email desse cadastrado, tento outro')


class FormCriarPost(FlaskForm):
    titulo = StringField('Escreva seu Titulo', validators=[DataRequired(), Length(2, 150)])
    corpo = TextAreaField('Escreva seu Post aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Enviar Post')