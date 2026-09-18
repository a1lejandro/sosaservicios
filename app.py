from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

BASE = os.path.dirname(os.path.abspath(__file__))
STOCK_FILE = os.path.join(BASE, 'stock.json')
VENTAS_FILE = os.path.join(BASE, 'ventas.json')

def cargar_json(path, default):
    try:
        if not os.path.exists(path):
            return default
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Limpia valores Undefined / None raros
            if isinstance(data, list):
                limpio = []
                for d in data:
                    if isinstance(d, dict):
                        # convierte todo a tipos simples
                        nd = {}
                        for k,v in d.items():
                            if v is None:
                                continue
                            # si es objeto raro, pasalo a string
                            try:
                                json.dumps(v)
                                nd[k]=v
                            except:
                                nd[k]=str(v)
                        limpio.append(nd)
                return limpio
            return data
    except:
        return default

def guardar_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    stock = cargar_json(STOCK_FILE, [])
    # Asegura que sea lista serializable
    stock_safe = []
    for i, p in enumerate(stock):
        if not isinstance(p, dict):
            continue
        stock_safe.append({
            'id': p.get('id', i),
            'producto': p.get('producto') or p.get('Producto') or p.get('nombre') or p.get('Nombre') or 'SIN NOMBRE',
            'cant': p.get('cant', p.get('Cantidad', p.get('stock', 0))),
            'precio': p.get('precio', p.get('Precio', 0)),
            'mostrador': p.get('mostrador', p.get('Mostrador', ''))
        })
    return render_template('index.html', stock=stock_safe)

@app.route('/api/guardar_stock', methods=['POST'])
def guardar_stock():
    data = request.get_json()
    guardar_json(STOCK_FILE, data)
    return jsonify({'ok': True})

@app.route('/api/vender', methods=['POST'])
def vender():
    data = request.get_json()
    items = data.get('items', [])
    # descuenta stock
    stock = cargar_json(STOCK_FILE, [])
    for item in items:
        for p in stock:
            pid = p.get('id')
            if pid == item.get('id'):
                try:
                    actual = int(p.get('cant', p.get('Cantidad', 0)) or 0)
                    vendido = int(item.get('cantidad', 1))
                    p['cant'] = max(0, actual - vendido)
                    if 'Cantidad' in p: p['Cantidad'] = p['cant']
                except:
                    pass
    guardar_json(STOCK_FILE, stock)
    # guarda venta
    ventas = cargar_json(VENTAS_FILE, [])
    ventas.append({
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'items': items
    })
    guardar_json(VENTAS_FILE, ventas)
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)