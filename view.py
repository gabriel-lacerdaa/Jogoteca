from flask import render_template, redirect, request, session, flash, url_for, send_from_directory
from app import app, db
from model import Jogos, Usuarios
import os
from helpers import salvarCapa, deletaCapa, FormularioJogo, FormularioLogin
from flask_bcrypt import check_password_hash

@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template("jogoteca.html", titulo="Jogos", jogos=lista)


@app.route('/novo')
def novo():
    if ("usuario_logado" in session) and (session["usuario_logado"] is not None):
        form = FormularioJogo()
        return render_template("novo.html", titulo="Novo Jogo", form=form)
    else:
        flash('É necessário fazer um login para incluir um novo jogo')
        return redirect(url_for('login', proxima=url_for('novo')))


@app.route('/criar', methods=["POST"])
def criar():
    jogo = Jogos.query.filter_by(nome=request.form["nome"]).first()
    if jogo:
        flash('Esse jogo já existe')
        return redirect(url_for('index'))
    else:
        form = FormularioJogo(request.form)
        if not form.validate_on_submit():
            return redirect(url_for('novo'))

        newJogo = Jogos(form.nome.data, form.categoria.data, form.console.data)
        db.session.add(newJogo)
        db.session.commit()
        arquivo = request.files['arquivo']
        if arquivo.filename != 'capa_padrao.jpg' and arquivo.filename != '':
            salvarCapa(newJogo, arquivo)
        
        return redirect(url_for('index'))


@app.route("/editar/<int:id>")
def editar(id):
    if ("usuario_logado" in session) and (session["usuario_logado"] != None):
        jogo = Jogos.query.filter_by(id=id).first()
        caminho_da_imagem = f'{app.config["UPLOAD_PATH"]}/Capa{str(jogo.id)}.jpg'
        #If para verificar se a imagem existe na pasta uploads
        if os.path.isfile(caminho_da_imagem):
            imagem = f'Capa{str(jogo.id)}.jpg'
        else:
            imagem = 'capa_padrao.jpg'

        form = FormularioJogo()
        form.nome.data = jogo.nome
        form.categoria.data = jogo.categoria
        form.console.data = jogo.console
        return render_template("editar.html", titulo="Editar Jogo", id=id, imagem=imagem, form=form)
    else:
        flash('É necessário fazer um login para editar um jogo')
        return redirect(url_for('login', proxima=url_for('editar',id=id)))


@app.route('/atualizar', methods=["POST"])
def atualizar():
    form = FormularioJogo(request.form)
    if form.validate_on_submit():  
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data
        db.session.add(jogo)
        db.session.commit()
        arquivo = request.files['arquivo']
        if arquivo.filename != '':
            salvarCapa(jogo, arquivo)
    return redirect(url_for('index'))


@app.route('/deletar<int:id>')
def deletar(id):
    if ("usuario_logado" in session) and (session["usuario_logado"] is not None):
        Jogos.query.filter_by(id=id).delete()
        db.session.commit()
        deletaCapa(id)
        return redirect(url_for('index'))
    else:
        flash('Necessário fazer o login para excluir um Jogo da lista')
        return redirect(url_for('login'))


@app.route('/login')
def login():
    proxima = request.args.get("proxima")
    form = FormularioLogin()
    return render_template("login.html", proxima=proxima, form=form)


@app.route('/autenticar', methods=["POST"])
def autenticar():
    form = FormularioLogin(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    if usuario:
                     #hash guardado no servidor | senha digitada
        senha = check_password_hash(usuario.senha, form.senha.data)
        if senha:
            session["usuario_logado"] = usuario.nickname
            flash(f'{session["usuario_logado"]} logado com sucesso!')
            proxima_pagina = request.form["proxima"]
            print(proxima_pagina, type(proxima_pagina))
            if proxima_pagina == 'None': proxima_pagina = None
            if proxima_pagina is None:
                return redirect(url_for('index'))
            else:
                return redirect(proxima_pagina)

    flash(' Usuario não existe, ou senha invalida')
    return redirect(url_for('login'))


@app.route("/logout")
def logout():
    session["usuario_logado"] = None
    flash('Usuario deslogado')
    return redirect(url_for('index'))


@app.route('/imagem/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

