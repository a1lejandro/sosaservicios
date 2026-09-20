# SOSA SERVICIO v8.5 FINAL - CLAVE Aa41412789 - LOGIN PROTEGIDO
from flask import Flask, render_template_string, request, session
import json, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "sosa-final-123-2026"
ARCH_PROD = "stock.json"
ARCH_VENTAS = "ventas.json"
ARCH_DEUDAS = "deudores.json"
CLAVE_ADMIN = "Aa41412789"
ALIAS_COBRO = "sosaservicios."
NOMBRE_NEGOCIO = "SOSA SERVICIO"

def cargar(ruta):
    if not os.path.exists(ruta) or os.path.getsize(ruta)==0: return []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except: return []
def guardar(ruta, d):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
def get_cant(p):
    try: return int(str(p.get("cant","0")).strip())
    except: return 0
def get_precio_int(p):
    try: return int(''.join(filter(str.isdigit, str(p.get("precio","0")))) or 0)
    except: return 0

LOGIN_HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{background:#0f172a;color:white;font-family:Arial;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}
.box{background:#1e293b;padding:30px;border-radius:15px;border:2px solid #38bdf8;text-align:center;width:90%;max-width:360px}
input{padding:12px;width:85%;border-radius:8px;border:none;margin:10px 0;text-align:center;font-size:18px}
.btn{padding:12px 20px;background:#38bdf8;border:none;border-radius:8px;font-weight:bold;cursor:pointer;width:90%}</style>
</head><body><div class="box"><h2>SOSA SERVICIO</h2><p>Solo acceso privado</p>
<form method="post"><input type="hidden" name="accion" value="login"><input name="clave" type="password" placeholder="Clave" required><br><button class="btn">ENTRAR</button>
{% if error %}<p style="color:#ff6b6b">{{error}}</p>{% endif %}</form></div></body></html>
"""

HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#0f172a;color:white;font-family:Arial;margin:0;padding:8px}
.box{max-width:1100px;margin:auto;background:#1e293b;border:2px solid #38bdf8;border-radius:15px;padding:12px}
.alias{background:#FFF9C4;color:black;padding:10px;border-radius:10px;text-align:center;font-weight:bold;font-size:18px}
.tab{cursor:pointer;padding:10px 14px;background:#334155;display:inline-block;border-radius:8px 8px 0 0;margin-right:4px}
.tab.active{background:#38bdf8;color:black;font-weight:bold}
.panel{display:none;background:white;color:black;padding:10px;border-radius:0 10px 10px 10px}
.panel.active{display:block}
.prod{padding:8px;margin:5px 0;border-radius:6px;display:flex;justify-content:space-between;align-items:center}
.verde{background:#C8E6C9}.azul{background:#BBDEFB}.rojo{background:#FFCDD2}
.btn{border:none;padding:7px 12px;border-radius:6px;font-weight:bold;cursor:pointer}
input{padding:8px;border-radius:5px;border:1px solid #ccc}
table{width:100%;border-collapse:collapse} th,td{border:1px solid #ccc;padding:6px;text-align:center;font-size:13px}
.carrito{background:#fffde7;border:2px solid #ff9800;padding:10px;border-radius:10px;color:black;margin-top:10px}
</style>
<script>function showTab(n){document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));document.getElementById('p'+n).classList.add('active');document.getElementById('t'+n).classList.add('active')}</script>
</head><body><div class="box">
<h2 style="text-align:center;margin:5px">{{negocio}} v8.5 SEGURO</h2>
<div class="alias">ALIAS: {{alias}} | <form method="post" style="display:inline"><input type="hidden" name="accion" value="logout"><button class="btn" style="background:#f44336;color:white;padding:4px 10px">Salir</button></form></div>
<div style="margin:10px 0"><span id="t1" class="tab active" onclick="showTab(1)">VENDER</span><span id="t2" class="tab" onclick="showTab(2)">Ventas ({{ventas|length}})</span><span id="t3" class="tab" onclick="showTab(3)">Deudores ({{deudores|length}})</span><span id="t4" class="tab" onclick="showTab(4)">Cierre</span></div>
<div id="p1" class="panel active">
<form method="get" style="margin-bottom:8px"><input type="hidden" name="tab" value="1"><input name="q" placeholder="Buscar codigo o nombre" value="{{q}}" style="width:60%"><label><input type="checkbox" name="sinstock" value="1" {{'checked' if sinstock else ''}}> Solo SIN STOCK</label><button class="btn" style="background:#38bdf8">Buscar</button></form>
<form method="post"><input type="hidden" name="accion" value="agregar_prod"><input name="codigo" placeholder="Codigo SOS-..." style="width:14%" required><input name="nombre" placeholder="Producto" style="width:22%" required><input name="cant" placeholder="Cant" style="width:8%" required><input name="precio" placeholder="Precio" style="width:10%" required><input name="ubicacion" placeholder="Ubic" style="width:8%"><input name="clave" placeholder="Clave" type="password" style="width:12%" required><button class="btn" style="background:#4CAF50;color:white">Agregar</button></form>
<div style="max-height:300px;overflow:auto;margin-top:8px">{% for p in productos %}<div class="prod {{'rojo' if p.cant==0 else 'azul' if p.cant<=3 else 'verde'}}"><div style="text-align:left"><b>{{p.codigo}}</b> - {{p.nombre}} | Cant:<b>{{p.cant}}</b> | ${{p.precio}}</div><div><form method="post" style="display:inline"><input type="hidden" name="accion" value="add_cart"><input type="hidden" name="idx" value="{{p.idx}}"><button class="btn" style="background:#FF9800">+ Carrito</button></form><form method="post" style="display:inline"><input type="hidden" name="accion" value="borrar_prod"><input type="hidden" name="idx" value="{{p.idx}}"><input name="clave" type="password" placeholder="clave" style="width:55px" required><button class="btn" style="background:#f44336;color:white">Borrar</button></form></div></div>{% endfor %}</div>
<div class="carrito"><h3>TOTAL: ${{total}} | Cliente:<form method="post" style="display:inline"><input type="hidden" name="accion" value="update_cliente"><input name="cliente" value="{{cliente}}" style="width:120px"></form></h3><table><tr><th>Codigo</th><th>Producto</th><th>Precio</th><th>Quitar</th></tr>{% for it in carrito %}<tr><td>{{it.codigo}}</td><td>{{it.nombre}}</td><td>${{it.precio}}</td><td><form method="post"><input type="hidden" name="accion" value="quitar_cart"><input type="hidden" name="cidx" value="{{loop.index0}}"><button class="btn">X</button></form></td></tr>{% endfor %}</table><form method="post" style="margin-top:8px"><input type="hidden" name="accion" value="vender"><button name="pago" value="1" class="btn" style="background:#2196F3;color:white;width:48%;padding:12px">VENDER EFECTIVO</button><button name="pago" value="2" class="btn" style="background:#22c55e;color:white;width:48%;padding:12px">VENDER TRANSFERENCIA</button></form>{% if mensaje %}<div style="background:#dcfce7;padding:10px;border-radius:8px;margin-top:8px;white-space:pre-line;font-weight:bold">{{mensaje}}</div>{% endif %}</div></div>
<div id="p2" class="panel"><form method="get"><input type="hidden" name="tab" value="2"><input name="qcli" placeholder="Buscar cliente" value="{{qcli}}" style="width:50%"><button class="btn">Buscar</button></form><table><tr><th>Fecha</th><th>Cliente</th><th>Producto</th><th>Precio</th><th>Pago</th><th>Anular</th></tr>{% for v in ventas_rev %}<tr><td>{{v.fecha}}</td><td>{{v.cliente}}</td><td>{{v.producto}}</td><td>{{v.precio}}</td><td>{{v.pago}}</td><td><form method="post"><input type="hidden" name="accion" value="anular_venta"><input type="hidden" name="v_idx" value="{{v.idx_real}}"><input name="clave" type="password" placeholder="clave" style="width:60px" required><button class="btn" style="background:#f44336;color:white">Anular</button></form></td></tr>{% endfor %}</table></div>
<div id="p3" class="panel"><form method="post"><input type="hidden" name="accion" value="add_deuda"><input name="nombre" placeholder="Nombre deudor" required><input name="monto" placeholder="Deuda $" required><input name="clave" type="password" placeholder="clave admin" required><button class="btn" style="background:#FF5722;color:white">AGREGAR FIADO</button></form><table style="margin-top:8px"><tr><th>Fecha</th><th>Nombre</th><th>Deuda</th><th>Pago</th></tr>{% for d in deudores_rev %}<tr><td>{{d.fecha}}</td><td>{{d.nombre}}</td><td>{{d.monto}}</td><td><form method="post"><input type="hidden" name="accion" value="del_deuda"><input type="hidden" name="d_idx" value="{{d.idx_real}}"><input name="clave" type="password" placeholder="clave" required><button class="btn" style="background:#4CAF50;color:white">PAGO</button></form></td></tr>{% endfor %}</table></div>
<div id="p4" class="panel"><h3>Cierre Hoy: {{hoy}}</h3><p>Ventas: {{cierre.cant}} | TOTAL: ${{cierre.total}} | EF: ${{cierre.ef}} | TRANSF: ${{cierre.tr}}</p><pre style="background:#f5f5f5;padding:10px;white-space:pre-wrap">{{cierre.det}}</pre></div>
</div><script>showTab({{tab}})</script></body></html>
"""

@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
        acc=request.form.get('accion','')
        if acc=='login':
            if request.form.get('clave','')==CLAVE_ADMIN: session['logado']=True
            else: return render_template_string(LOGIN_HTML, error="Clave incorrecta")
        elif acc=='logout':
            session.pop('logado',None)
            return render_template_string(LOGIN_HTML, error=None)
    if not session.get('logado'):
        return render_template_string(LOGIN_HTML, error=None)

    productos=cargar(ARCH_PROD); ventas=cargar(ARCH_VENTAS); deudores=cargar(ARCH_DEUDAS)
    if 'carrito' not in session: session['carrito']=[]
    if 'cliente' not in session: session['cliente']="Mostrador"
    q=request.args.get('q',''); qcli=request.args.get('qcli',''); sinstock=request.args.get('sinstock')=='1'; tab=int(request.args.get('tab','1')); mensaje=None
    if request.method=='POST':
        acc=request.form.get('accion'); clave=request.form.get('clave','')
        if acc=='agregar_prod':
            if clave!=CLAVE_ADMIN: mensaje="Clave incorrecta"
            else:
                productos.append({"codigo":request.form.get('codigo','').strip(),"nombre":request.form.get('nombre','').strip(),"cant":request.form.get('cant','').strip(),"precio":request.form.get('precio','').strip(),"ubicacion":request.form.get('ubicacion','').strip()})
                guardar(ARCH_PROD, productos); mensaje="Producto agregado"; tab=1
        elif acc=='borrar_prod':
            if clave!=CLAVE_ADMIN: mensaje="Clave incorrecta"
            else:
                idx=int(request.form.get('idx',0))
                if 0<=idx<len(productos): del productos[idx]; guardar(ARCH_PROD, productos); mensaje="Borrado"
            tab=1
        elif acc=='add_cart':
            idx=int(request.form.get('idx',0))
            if 0<=idx<len(productos):
                p=productos[idx]
                if get_cant(p)<=0: mensaje=f"Sin stock: {p['nombre']}"
                else: session['carrito'].append({"codigo":p['codigo'],"nombre":p['nombre'],"precio":p['precio']}); session.modified=True
            tab=1
        elif acc=='quitar_cart':
            cidx=int(request.form.get('cidx',0)); cart=session.get('carrito',[])
            if 0<=cidx<len(cart): del cart[cidx]; session['carrito']=cart
            tab=1
        elif acc=='update_cliente': session['cliente']=request.form.get('cliente','Mostrador'); tab=1
        elif acc=='vender':
            cart=session.get('carrito',[])
            if not cart: mensaje="Carrito vacio"
            else:
                pago=request.form.get('pago','1'); medio="EFECTIVO" if pago=="1" else f"TRANSFERENCIA a {ALIAS_COBRO}"
                cliente=session.get('cliente','Mostrador'); fecha=datetime.now().strftime("%d/%m/%Y %H:%M"); total=0
                for it in cart:
                    for p in productos:
                        if p['codigo']==it['codigo']:
                            cant=get_cant(p)
                            if cant>0: p['cant']=str(cant-1); total+=get_precio_int(p); ventas.append({"fecha":fecha,"cliente":cliente,"producto":p['nombre'],"precio":p['precio'],"codigo":p['codigo'],"pago":medio})
                            break
                guardar(ARCH_PROD, productos); guardar(ARCH_VENTAS, ventas); session['carrito']=[]; mensaje=f"VENTA {medio} ${total} OK!"
            tab=1
        elif acc=='anular_venta':
            if clave!=CLAVE_ADMIN: mensaje="Clave incorrecta"
            else:
                v_idx=int(request.form.get('v_idx',0))
                if 0<=v_idx<len(ventas):
                    v=ventas[v_idx]
                    for p in productos:
                        if p['codigo']==v.get('codigo') or p['nombre']==v.get('producto'): p['cant']=str(get_cant(p)+1); break
                    del ventas[v_idx]; guardar(ARCH_PROD, productos); guardar(ARCH_VENTAS, ventas); mensaje="Venta anulada"
            tab=2
        elif acc=='add_deuda':
            if clave!=CLAVE_ADMIN: mensaje="Clave incorrecta"
            else: deudores.append({"fecha":datetime.now().strftime("%d/%m/%Y %H:%M"),"nombre":request.form.get('nombre',''),"monto":request.form.get('monto',''),"telefono":"","direccion":""}); guardar(ARCH_DEUDAS, deudores); mensaje="Deudor agregado"; tab=3
        elif acc=='del_deuda':
            if clave!=CLAVE_ADMIN: mensaje="Clave incorrecta"
            else:
                d_idx=int(request.form.get('d_idx',0))
                if 0<=d_idx<len(deudores): del deudores[d_idx]; guardar(ARCH_DEUDAS, deudores); mensaje="Deuda pagada"; tab=3

    prod_list=[]; q_low=q.lower()
    for idx,p in enumerate(productos):
        cant=get_cant(p)
        if sinstock and cant!=0: continue
        if q_low and q_low not in (p.get('nombre','').lower()+p.get('codigo','').lower()): continue
        prod_list.append({"idx":idx,"codigo":p.get('codigo',''),"nombre":p.get('nombre',''),"cant":cant,"precio":p.get('precio',''),"ubicacion":p.get('ubicacion','')})
    ventas_rev=[]; qcli_low=qcli.lower()
    for idx in range(len(ventas)-1, -1, -1):
        v=ventas[idx]
        if qcli_low and qcli_low not in v.get('cliente','').lower(): continue
        ventas_rev.append({"idx_real":idx,"fecha":v.get('fecha',''),"cliente":v.get('cliente',''),"producto":v.get('producto',''),"precio":v.get('precio',''),"pago":v.get('pago','')})
    deudores_rev=[]
    for idx in range(len(deudores)-1, -1, -1):
        d=deudores[idx]; deudores_rev.append({"idx_real":idx,"fecha":d.get('fecha',''),"nombre":d.get('nombre',''),"monto":d.get('monto','')})
    total=sum(get_precio_int({"precio":it.get('precio','0')}) for it in session.get('carrito',[]))
    hoy=datetime.now().strftime("%d/%m/%Y"); tot=0; tot_ef=0; tot_tr=0; cant=0; det=""
    for v in ventas:
        if hoy in v.get('fecha',''): m=get_precio_int(v); tot+=m; tot_ef+=m if "EFECTIVO" in v.get('pago','') else 0; tot_tr+=0 if "EFECTIVO" in v.get('pago','') else m; cant+=1; det+=f"{v['fecha']} {v['cliente']} {v['producto']} ${v['precio']} [{v.get('pago','')}]\n"
    cierre={"total":tot,"ef":tot_ef,"tr":tot_tr,"cant":cant,"det":det or "Sin ventas hoy"}
    return render_template_string(HTML, negocio=NOMBRE_NEGOCIO, alias=ALIAS_COBRO, productos=prod_list, ventas=ventas, ventas_rev=ventas_rev, deudores=deudores, deudores_rev=deudores_rev, carrito=session.get('carrito',[]), total=total, mensaje=mensaje, q=q, qcli=qcli, sinstock=sinstock, tab=tab, cliente=session.get('cliente','Mostrador'), hoy=hoy, cierre=cierre)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=10000)
