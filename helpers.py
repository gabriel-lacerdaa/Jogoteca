import os
from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField

# Classe para validar o formulario
class FormularioJogo(FlaskForm):
    nome = StringField('Nome Do Jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')


class FormularioLogin(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=5, max=100)])
    login = SubmitField('Login')


def salvarCapa(Jogo, arquivo):
    uploads_path = app.config["UPLOAD_PATH"]
    arquivo.save(f'{uploads_path}/Capa{Jogo.id}.jpg')    


def deletaCapa(id):
    caminho_da_imagem = f'{app.config["UPLOAD_PATH"]}/Capa{str(id)}.jpg'
    if os.path.isfile(caminho_da_imagem):
        os.remove(os.path.join(app.config["UPLOAD_PATH"], f'Capa{str(id)}.jpg'))
