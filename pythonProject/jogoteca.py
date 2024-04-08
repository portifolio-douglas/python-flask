from flask import Flask, render_template, request, redirect, session, flash


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


jogo1 = Jogo("God of War: Ragnarök", "Rack n Slash", "PS4/PS5")
jogo2 = Jogo("Call of Duty: Warzone", "Battle Royale", "PS4/PS5")
jogo3 = Jogo("Horizon: Forbbiden West", "Aventura/RPG", "PS4/PS5")
lista = [jogo1, jogo2, jogo3]

app = Flask(__name__)
app.secret_key = 'alura'

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)


@app.route("/novo")
def novo():
    return render_template("novo.html", titulo="Novo Jogo")


@app.route("/criar", methods=['POST',])
def criar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect('/')


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/autenticar", methods=['POST',])
def autenticas():
    if 'alohomora' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash(session['usuario_logado'] + ' logado com sucesso!')
        return redirect('/')
    else:
        flash("Usuário não encontrado")
        return redirect('/login')

app.run(host="0.0.0.0", port=8080, debug=True)
