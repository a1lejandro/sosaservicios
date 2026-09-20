from flask import Flask, render_template_string, request, redirect
import json, os
from datetime import datetime

app = Flask(__name__)
ALIAS = "sosaservicios.mp"

def cargar(f):
    if not os.path.exists(f): return []
    try:
        with open(f,"r",encoding="utf-8") as x: return json.load(x)
    except: return []
def guardar(f,d):
    with open(f,"w",encoding="utf-8") as x: json.dump(d,x,ensure_ascii=False,indent=2)

HTML = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#0f172a;color:white;font-family:Arial;text-align:center}
.box{border:2px solid #38bdf8;padding:20px;border-radius:20px;max-width:500px;margin:20px auto;background:#1e293b}
h1{font-size:50px;letter-spacing:5px} p{font-size:20px;color:#38bdf8}
.btn{padding:15px 25px;font-size:18px;margin:10px;background:#38bdf8;border:none;border-radius:10px;font-weight:bold}
.alias{background:#FFF9C4;color:black;padding:15px;font-size:22px;font-weight:bold;border-radius:10px;margin:15px 0}
</style></head><body>
<div class="box">
<h1>SOSA SISTEMAS</h1>
<p>Servicio Técnico Profesional</p>
<p>Corrientes - Argentina</p>
<div class="alias">ALIAS TRANSFERENCIA:<br>{{alias}}</div>
<h3>TOTAL: ${{total}}</h3>
<form method="post">
<button class="btn" name="pago" value="1">1 - EFECTIVO</button>
<button class="btn" name="pago" value="2">2 - TRANSFERENCIA</button>
</form>
{% if mensaje %}<div style="background:white;color:black;padding:15px;border-radius:10px;margin-top:15px;font-weight:bold">{{mensaje}}</div>{% endif %}
</div>
</body></html>
"""

@app.route('/', methods=['GET','POST'])
def inicio():
    total = 100  # ejemplo, después conectamos con tu stock.json
    mensaje = None
    if request.method == 'POST':
        pago = request.form.get('pago')
        if pago == '1':
            mensaje = f"COBRO EFECTIVO ${total} - Gracias!"
        else:
            mensaje = f"Que transfiera ${total} a ALIAS: {ALIAS} - Una vez transferido avisar."
    return render_template_string(HTML, alias=ALIAS, total=total, mensaje=mensaje)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
