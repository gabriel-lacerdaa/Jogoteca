from flask import render_template, redirect, request, session, flash, url_for, send_from_directory
from app import app, db
from model import Jogos, Usuarios
import os


@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template("jogoteca.html", titulo="Jogos", jogos=lista)


@app.route('/novo')
def novo():
    if ("usuario_logado" in session) and (session["usuario_logado"] is not None):
        return render_template("novo.html", titulo="Novo Jogo")
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
        newJogo = Jogos(nome=request.form["nome"], categoria=request.form["categoria"], console=request.form["console"])
        db.session.add(newJogo)
        db.session.commit()
        #Criar função para salvar
        uploads_path = app.config["UPLOAD_PATH"]
        arquivo = request.files['arquivo']
        arquivo.save(f'{uploads_path}/Capa{newJogo.id}.jpg')    
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
        print(imagem)
        return render_template("editar.html", titulo="Editar Jogo", jogo=jogo, imagem=imagem)
    else:
        flash('É necessário fazer um login para editar um jogo')
        return redirect(url_for('login', proxima=url_for('editar',id=id)))


@app.route('/atualizar', methods=["POST"])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome = request.form["nome"]
    jogo.categoria = request.form["categoria"]
    jogo.console = request.form["console"]
    db.session.add(jogo)
    db.session.commit()
    #Criar função para salvar
    uploads_path = app.config["UPLOAD_PATH"]
    arquivo = request.files['arquivo']
    arquivo.save(f'{uploads_path}/Capa{jogo.id}.jpg')
    return redirect(url_for('index'))


@app.route('/deletar<int:id>')
def deletar(id):
    if ("usuario_logado" in session) and (session["usuario_logado"] is not None):
        Jogos.query.filter_by(id=id).delete()
        db.session.commit()
        caminho_da_imagem = f'{app.config["UPLOAD_PATH"]}/Capa{str(id)}.jpg'
        if os.path.isfile(caminho_da_imagem):
            os.remove(os.path.join(app.config["UPLOAD_PATH"], f'Capa{str(id)}.jpg'))
        return redirect(url_for('index'))
    else:
        flash('Necessário fazer o login para excluir um Jogo da lista')
        return redirect(url_for('login'))


@app.route('/login')
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", proxima=proxima)


@app.route('/autenticar', methods=["POST"])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if usuario.senha == request.form["senha"]:
            session["usuario_logado"] = usuario.nickname
            flash(f'{session["usuario_logado"]} logado com sucesso!')
            proxima_pagina = request.form["proxima"]
            print(proxima_pagina, type(proxima_pagina))
            if proxima_pagina == 'None': proxima_pagina = None
            if proxima_pagina is None:
                return redirect(url_for('index'))
            else:
                return redirect(proxima_pagina)
    else:
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

