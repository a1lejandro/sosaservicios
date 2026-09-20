from flask import Flask, render_template_string, request, session, redirect
import os

app = Flask(__name__)
app.secret_key = "sosa-sistemas-2026"

ALIAS = "sosaservicios.mp"

# TU STOCK - podes editarlo acá
PRODUCTOS = [
    {"id": 1, "nombre": "Cable USB", "precio": 2000, "stock": 20},
    {"id": 2, "nombre": "Cargador Samsung", "precio": 8500, "stock": 15},
    {"id": 3, "nombre": "Auriculares", "precio": 5000, "stock": 10},
    {"id": 4, "nombre": "Vidrio Templado", "precio": 2500, "stock": 30},
    {"id": 5, "nombre": "Funda Silicona", "precio": 4000, "stock": 25},
]

HTML_COMPLETO = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#0f172a;color:white;font-family:Arial;margin:0;padding:10px}
.box{border:2px solid #38bdf8;padding:15px;border-radius:15px;max-width:600px;margin:10px auto;background:#1e293b}
h1{text-align:center;letter-spacing:3px;margin:5px}
.alias{background:#FFF9C4;color:black;padding:12px;font-weight:bold;border-radius:10px;text-align:center;font-size:18px;margin:10px 0}
.prod{background:#334155;padding:10px;margin:5px 0;border-radius:8px;display:flex;justify-content:space-between;align-items:center}
.btn{background:#38bdf8;border:none;padding:8px 12px;border-radius:6px;font-weight:bold;cursor:pointer}
.btn-cobrar{width:100%;padding:15px;font-size:18px;margin:5px 0}
.carrito{background:white;color:black;padding:10px;border-radius:10px;margin-top:15px}
</style></head><body>
<div class="box">
<h1>SOSA SISTEMAS</h1>
<p style="text-align:center;color:#38bdf8">Servicio Tecnico - Corrientes</p>
<div class="alias">ALIAS: {{alias}}</div>

<h3>Productos</h3>
<form method="get"><input name="q" placeholder="Buscar producto..." value="{{q}}" style="width:70%;padding:8px;border-radius:5px"><button class="btn">Buscar</button></form>

{% for p in productos %}
<div class="prod">
<span>{{p.nombre}} - ${{p.precio}} (Stock: {{p.stock}})</span>
<form method="post" style="margin:0"><input type="hidden" name="add" value="{{p.id}}"><button class="btn">+</button></form>
</div>
{% endfor %}

<div class="carrito">
<h3>Carrito: ${{total}}</h3>
{% for item in carrito %}<div>{{item.nombre}} x{{item.cant}} - ${{item.precio * item.cant}}</div>{% endfor %}
{% if total>0 %}
<form method="post">
<button name="pago" value="1" class="btn btn-cobrar">1 - EFECTIVO - Cobrar ${{total}}</button>
<button name="pago" value="2" class="btn btn-cobrar" style="background:#22c55e">2 - TRANSFERENCIA a {{alias}}</button>
</form>
{% endif %}
{% if mensaje %}<div style="background:#dcfce7;color:black;padding:10px;border-radius:5px;margin-top:10px;font-weight:bold;white-space:pre-line">{{mensaje}}</div>{% endif %}
</div>

<form method="post"><button name="limpiar" value="1" class="btn" style="background:#ef4444;width:100%;margin-top:10px">Limpiar Carrito</button></form>
</div>
</body></html>
"""

@app.route('/', methods=['GET','POST'])
def inicio():
    q = request.args.get('q','').lower()
    if 'carrito' not in session: session['carrito'] = []
    
    mensaje = None
    if request.method == 'POST':
        if request.form.get('add'):
            pid = int(request.form.get('add'))
            prod = next((x for x in PRODUCTOS if x['id']==pid), None)
            if prod:
                cart = session['carrito']
                ex = next((x for x in cart if x['id']==pid), None)
                if ex: ex['cant']+=1
                else: cart.append({"id":pid,"nombre":prod['nombre'],"precio":prod['precio'],"cant":1})
                session['carrito']=cart
        if request.form.get('limpiar'):
            session['carrito']=[]
        if request.form.get('pago'):
            total = sum(x['precio']*x['cant'] for x in session['carrito'])
            if request.form.get('pago')=='1':
                mensaje = f"VENTA EFECTIVO ${total} CONFIRMADA!\nGracias!"
            else:
                mensaje = f"VENTA TRANSFERENCIA ${total}\nQue transfiera a:\n{ALIAS}\n\nEsperar comprobante."
            session['carrito']=[]

    total = sum(x['precio']*x['cant'] for x in session.get('carrito',[]))
    prods = [p for p in PRODUCTOS if q in p['nombre'].lower()] if q else PRODUCTOS
    return render_template_string(HTML_COMPLETO, alias=ALIAS, productos=prods, carrito=session.get('carrito',[]), total=total, mensaje=mensaje, q=q)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
