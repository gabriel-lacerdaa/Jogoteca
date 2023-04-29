#Aqui vou colocar todas as rotas relacionadas ao usuario
from flask import render_template, redirect, request, session, flash, url_for
from app import app
from model import Usuarios
from helpers import FormularioLogin
from flask_bcrypt import check_password_hash


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