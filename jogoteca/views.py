from flask import flash, redirect, render_template, request, session, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos, Usuarios


@app.route("/")
def index():
    lista = Jogos.query.order_by(Jogos.nome)
    return render_template("lista.html", titulo="Jogos", jogos=lista)


@app.route("/novo_jogo")
def novo():
    if "usuario_logado" not in session or session["usuario_logado"] is None:
        return redirect(url_for("login", proxima=url_for("novo")))
    return render_template("novo.html", titulo="Novo Jogo")


@app.route("/criar", methods=["POST",])
def criar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash("Este jogo já existe")
        return redirect(url_for('index'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}')

    return redirect(url_for("index"))


@app.route("/editar/<int:id>")
def editar(id):
    if "usuario_logado" not in session or session["usuario_logado"] is None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = Jogos.query.filter_by(id=id).first()

    return render_template("editar.html", titulo="Editar Jogo", jogo=jogo)


@app.route("/atualizar", methods=["POST",])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']

    db.session.add(jogo)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    if "usuario_logado" not in session or session["usuario_logado"] is None:
        return redirect(url_for('login'))

    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash("Jogo deletado!")

    return redirect(url_for('index'))


@app.route("/login")
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", proxima=proxima)


@app.route('/autenticar', methods=["POST", ], )
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form["usuario"]).first()
    if usuario:
        if request.form["senha"] == usuario.senha:
            session["usuario_logado"] = usuario.nickname
            session["usuario_logado"] = request.form["usuario"]
            flash(usuario.nickname + " logado com sucesso!")
            proxima_pagina = request.form["proxima"]
            return redirect(proxima_pagina)
        else:
            flash("Usuário não encontrado")
            return redirect(url_for("/login"))


@app.route("/logout")
def logout():
    session["usuario_logado"] = None
    flash("Logout efetuado")
    return redirect(url_for("index"))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)