from flask import Flask, render_template, request, session
from math import ceil

app = Flask(__name__)
app.secret_key = "DJIKSAHDIWIMDIAMSID129109312093890SADO/;a/./ds.ad.sADhuASHDUHW*!@SI"
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def index():
    session["unidade"] = ["km", "h"]
    return render_template("index.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/posicao")
def posicao():
    if request.method == "GET":
        if session["unidade"][0] == "m":
            session["unidade"] = ["km", "h"]
        else:
            session["unidade"] = ["m", "s"]
    return render_template("posicao.html", unidade=session.get("unidade"))

@app.route("/velocidade")
def velocidade():
    if request.method == "GET":
        if session["unidade"][0] == "m":
            session["unidade"] = ["km", "h"]
        else:
            session["unidade"] = ["m", "s"]
    return render_template("velocidade.html", unidade=session.get("unidade"))

@app.route("/espaco")
def espaco():
    if request.method == "GET":
        if session["unidade"][0] == "m":
            session["unidade"] = ["km", "h"]
        else:
            session["unidade"] = ["m", "s"]
    return render_template("espaco.html", unidade=session.get("unidade"))

@app.route("/result", methods=["POST"])
def result():
    equacao = ""
    data = []
    #caso o tempo seja omitido de alguma forma, há um valor padrão
    tempo = [_ for _ in range(11)]
    label = [str(_)+session["unidade"][1] for _ in range(11)]

    #criação do eixo do tempo no gráfico + tratamento de valores com vírgula
    t = request.form.get("t")
    if t:
        if "," in t:
            t = t.replace(",", ".")

        if "-" in t:
            t = t[1::]

        t_arredondado = ceil(float(t))
        label = [str(_)+session["unidade"][1] for _ in range(0, t_arredondado)]
        tempo = [_ for _ in range(0, t_arredondado)]

        label.append(t+session["unidade"][1])
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

    elif ac and v0:
        equacao = "Velocidade"
        for t in tempo:
            acXt = float(ac)*t
            data.append(float(v0)+ acXt)
    
    elif v:
        equacao = "Posição"
        for t in tempo:
            vXt = float(v)*t
            data.append(float(s0) + vXt)

    return render_template("result.html", label=label, data=data, equacao=equacao, unidade=session.get("unidade"))

#essa rota serve para lidar com erros que só vão acontecer caso tentem editar o html
@app.errorhandler(500)
def error_page(error):
    return render_template("error.html"), 500