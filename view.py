from flask import render_template, redirect, request, session, flash, url_for
from app import app, db
from model import Jogos, Usuarios

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
        return redirect(url_for(index))
    else:
        newJogo = Jogos(nome=request.form["nome"], categoria=request.form["categoria"], console=request.form["console"])
        db.session.add(newJogo)
        db.session.commit()
        return redirect(url_for('index'))


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
