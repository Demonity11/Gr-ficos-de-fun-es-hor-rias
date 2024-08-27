from flask import Flask, render_template, request

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/posicao")
def posicao():
    return render_template("posicao.html")

@app.route("/velocidade")
def velocidade():
    return render_template("velocidade.html")

@app.route("/espaco")
def espaco():
    return render_template("espaco.html")