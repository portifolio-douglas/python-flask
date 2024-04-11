from flask import Flask, render_template, request, redirect, session, flash, url_for


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


class Usuario():
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('Douglas Henrique', 'Tilisco', 'tiliskin')
usuario2 = Usuario('Rafael França', 'Tilibins', 'tilambucano')
usuario3 = Usuario('Mateus Oliveira', 'Tilibamba', 'eaiwolfinhos')
usuarios = {
    usuario1.nickname: usuario1,
    usuario2.nickname: usuario2,
    usuario3.nickname: usuario3
}

jogo1 = Jogo("God of War: Ragnarök", "Rack n Slash", "PS4/PS5")
jogo2 = Jogo("Call of Duty: Warzone", "Battle Royale", "PS4/PS5")
jogo3 = Jogo("Horizon: Forbbiden West", "Aventura/RPG", "PS4/PS5")
lista = [jogo1, jogo2, jogo3]

app = Flask(__name__)
app.secret_key = 'alura'

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)


@app.route("/novo_jogo")
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template("novo.html", titulo="Novo Jogo")


@app.route("/criar", methods=['POST',])
def criar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))


@app.route("/login")
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route("/autenticar", methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            session['usuario_logado'] = request.form['usuario']
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash("Usuário não encontrado")
            return redirect(url_for('/login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
