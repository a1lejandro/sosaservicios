from flask import Flask
app = Flask(__name__)

@app.route('/')
def inicio():
    return """
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #0f172a; color: white; font-family: Arial; text-align: center; padding-top: 100px; }
        h1 { font-size: 60px; letter-spacing: 5px; }
        p { font-size: 20px; color: #38bdf8; }
        .box { border: 2px solid #38bdf8; display: inline-block; padding: 40px; border-radius: 20px; }
    </style>
    </head>
    <body>
        <div class="box">
            <h1>SOSA SISTEMAS</h1>
            <p>Servicio Técnico Profesional</p>
            <p>Corrientes - Argentina</p>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run()
