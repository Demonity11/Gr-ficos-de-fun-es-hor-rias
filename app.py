from flask import Flask, render_template, request
from math import ceil

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

@app.route("/result", methods=["POST"])
def result():
    t = request.form.get("t")
    if "." in t or "," in t:
        t = t.replace(",", ".") if "," in t else t
        tempo_decimal = True

    t_arredondado = ceil(float(t))
    tempo = [str(_)+"s" for _ in range(0, t_arredondado)]
    tempo.append(t+"s")

    s0 = request.form.get("s0")
    if "." in s0 or "," in s0:
        s0 = s0.replace(",", ".") if "," in s0 else s0

    s0_arredondado = ceil(float(s0))
    s0_ = s0_arredondado - float(s0)
    
    ac = request.form.get("ac")
    if "." in ac or "," in ac:
        ac = ac.replace(",", ".") if "," in ac else ac

    ac_arredondado = ceil(float(ac))
    ac_ = ac_arredondado - float(ac) 

    if request.form.get("ac") and request.form.get("s0") and request.form.get("v0"):
        s0 = request.form.get("s0")
        ac = request.form.get("ac")

    elif request.form.get("ac") and request.form.get("s0"):
        velocidade = [s0]
        multiplicador = 1
        for _ in range(s0_arredondado, s0_arredondado + ac_arredondado*len(tempo), ac_arredondado):
            if _ > s0_arredondado:
                velocidade.append(_ - (ac_*multiplicador + s0_))
                multiplicador += 1

        if tempo_decimal:
            velocidade[-1] = float(s0) + float(ac)*float(t)
   
        return render_template("result.html", tempo=tempo, velocidade=velocidade)