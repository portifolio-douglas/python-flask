from flask import Flask, render_template

app = Flask(__name__)

class Jogo():
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

@app.route('/inicio')
def ola():
    jogo1 = Jogo('God of War: Ragnarök', 'Rack n Slash', 'PS4/PS5')
    jogo2 = Jogo('Call of Duty: Warzone', 'Battle Royale', 'PS4/PS5')
    jogo3 = Jogo('Horizon: Forbbiden West', 'Aventura/RPG', 'PS4/PS5')
    lista = [jogo1, jogo2, jogo3]
    return render_template('lista.html', titulo='Jogos', jogos=lista)

app.run(host='0.0.0.0', port=8080)