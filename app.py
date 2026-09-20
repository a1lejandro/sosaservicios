from flask import Flask, render_template_string, request, session
import json, os

app = Flask(__name__)
app.secret_key = "sosa-2026"
ALIAS = "sosaservicios.mp"

def cargar_stock():
    try:
        with open('stock.json','r', encoding='utf-8') as f:
            data = json.load(f)
            # Normalizamos tu formato
            productos=[]
            for i, p in enumerate(data):
                precio = p.get('precio','0')
                # limpia $ y puntos
                precio_limpio = int(''.join(filter(str.isdigit, str(precio))) or 0)
                productos.append({
                    "id": i,
                    "nombre": p.get('nombre',''),
                    "precio": precio_limpio,
                    "cant": p.get('cant','0'),
                    "codigo": p.get('codigo',''),
                    "categoria": p.get('categoria',''),
                    "ubicacion": p.get('ubicacion','')
                })
            return productos
    except Exception as e:
        return [{"id":0,"nombre":f"Error leyendo stock: {e}","precio":0,"cant":"0","codigo":"","categoria":"","ubicacion":""}]

HTML = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#0f172a;color:white;font-family:Arial;margin:0;padding:10px}
.box{border:2px solid #38bdf8;padding:15px;border-radius:15px;max-width:700px;margin:auto;background:#1e293b}
.alias{background:#FFF9C4;color:black;padding:12px;font-weight:bold;border-radius:10px;text-align:center;font-size:20px;margin:10px 0}
.prod{background:#334155;padding:10px;margin:6px 0;border-radius:8px;display:flex;justify-content:space-between;align-items:center}
.btn{background:#38bdf8;border:none;padding:8px 14px;border-radius:6px;font-weight:bold}
.btn-cobrar{width:100%;padding:15px;font-size:18px;margin:6px 0}
.carrito{background:white;color:black;padding:10px;border-radius:10px;margin-top:15px}
input{padding:10px;border-radius:5px;border:none}
</style></head><body>
<div class="box">
<h1 style="text-align:center">SOSA SISTEMAS</h1>
<div class="alias">ALIAS: {{alias}}</div>

<form method="get"><input name="q" placeholder="Buscar... secador, cocina, etc" value="{{q}}" style="width:70%"><button class="btn">Buscar</button></form>
<p>{{productos|length}} productos - Buscando: {{q or 'todos'}}</p>

{% for p in productos[:100] %}
<div class="prod">
<div><b>{{p.nombre}}</b><br><small>{{p.codigo}} | {{p.categoria}} | Cant: {{p.cant}} | Ubic: {{p.ubicacion}}</small><br>${{p.precio}}</div>
<form method="post"><input type="hidden" name="add" value="{{p.id}}"><button class="btn">+ Agregar</button></form>
</div>
{% endfor %}

<div class="carrito">
<h3>Carrito: ${{total}}</h3>
{% for it in carrito %}<div>{{it.nombre}} x{{it.cant}} = ${{it.precio*it.cant}}</div>{% endfor %}
{% if total>0 %}
<form method="post">
<button name="pago" value="1" class="btn btn-cobrar" style="background:#0f172a;color:white">1 - EFECTIVO ${{total}}</button>
<button name="pago" value="2" class="btn btn-cobrar" style="background:#22c55e">2 - TRANSFERENCIA a {{alias}} - ${{total}}</button>
</form>
{% endif %}
{% if mensaje %}<div style="background:#dcfce7;padding:12px;border-radius:8px;margin-top:10px;white-space:pre-line;font-weight:bold">{{mensaje}}</div>{% endif %}
<form method="post"><button name="limpiar" value="1" class="btn" style="background:#ef4444;width:100%;margin-top:10px;color:white">Vaciar carrito</button></form>
</div>
</div></body></html>
"""

@app.route('/', methods=['GET','POST'])
def index():
    stock = cargar_stock()
    q = request.args.get('q','').lower()
    if 'carrito' not in session: session['carrito']=[]
    mensaje=None
    if request.method=='POST':
        if request.form.get('add'):
            pid=int(request.form.get('add'))
            prod=next((x for x in stock if x['id']==pid), None)
            if prod:
                cart=session['carrito']
                ex=next((x for x in cart if x['id']==pid), None)
                if ex: ex['cant']+=1
                else: cart.append({"id":pid,"nombre":prod['nombre'],"precio":prod['precio'],"cant":1})
                session['carrito']=cart
        if request.form.get('limpiar'): session['carrito']=[]
        if request.form.get('pago'):
            total=sum(x['precio']*x['cant'] for x in session['carrito'])
            if request.form.get('pago')=='1':
                mensaje=f"VENTA EFECTIVO ${total} CONFIRMADA"
            else:
                mensaje=f"VENTA TRANSFERENCIA ${total}\n\nQUE TRANSFIERA A:\n{ALIAS}\n\nEsperar comprobante."
            session['carrito']=[]
    total=sum(x['precio']*x['cant'] for x in session.get('carrito',[]))
    filtrados=[p for p in stock if q in p['nombre'].lower() or q in p['codigo'].lower() or q in p['categoria'].lower()] if q else stock
    return render_template_string(HTML, alias=ALIAS, productos=filtrados, carrito=session.get('carrito',[]), total=total, mensaje=mensaje, q=q)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=10000)
