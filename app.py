from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
#secret key para colocar uma camada de criptografia, para os cookies
app.secret_key = 'senhamuitoultasecreta'

infos_de_conexao = {
    'SGBD': 'mysql+mysqlconnector',
    'usuario': 'root',
    'senha': 'admin',
    'servidor': 'localhost',
    'database': 'jogoteca'
}

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD = infos_de_conexao["SGBD"],
    usuario = infos_de_conexao["usuario"],
    senha = infos_de_conexao["senha"],
    servidor = infos_de_conexao["servidor"],
    database = infos_de_conexao["database"],
    )
db = SQLAlchemy(app)

class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Name {self.name}>'


class Usuarios(db.Model):
    nome = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(8), primary_key=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Usuario(nome='{self.nome}', nickname='{self.nickname}', senha='{self.senha}')"


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


if __name__ == "__main__":
    # trecho da app
    app.run(host='localhost', debug=True)
