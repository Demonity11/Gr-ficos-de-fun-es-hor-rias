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
    equacao = ""
    data = []

    #criação do eixo do tempo no gráfico + tratamento de valores com vírgula
    t = request.form.get("t")
    if "." in t or "," in t:
        t = t.replace(",", ".") if "," in t else t

    t_arredondado = ceil(float(t))
    label = [str(_)+"s" for _ in range(0, t_arredondado)]
    tempo = [_ for _ in range(0, t_arredondado)]

    label.append(t+"s")
    tempo.append(float(t))

    #tratamento dos valores para que o python possa ler sem problemas
    s0 = request.form.get("s0")
    if s0:
        if "," in s0:
            s0 = s0.replace(",", ".")
    
    ac = request.form.get("ac")
    if ac:
        if "," in ac:
            ac = ac.replace(",", ".")

    v0 = request.form.get("v0")
    if v0:
        if "," in v0:
            v0 = v0.replace(",", ".")

    v = request.form.get("v")
    if v:
        if "," in v:
            v = v.replace(",", ".")

    #condição para determinação de qual equação estamos trabalhando + construção do eixo y que pode ser
    #espaço, velocidade ou posição.
    if ac and s0 and v0:
        equacao = "Espaço"
        for t in tempo:
            v0Xt = float(v0)*t
            acXt2 = (float(ac)/2)*t**2
            data.append(float(s0) + v0Xt + acXt2)

    elif ac and s0:
        equacao = "Velocidade"
        for t in tempo:
            acXt = float(ac)*t
            data.append(float(s0)+ acXt)
    
    elif v:
        equacao = "Posição"
        for t in tempo:
            vXt = float(v)*t
            data.append(float(s0) + vXt)
   
    return render_template("result.html", label=label, data=data, equacao=equacao)