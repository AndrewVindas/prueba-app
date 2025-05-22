#!/usr/bin/env python
from flask import Flask, request, jsonify, send_file
from models import db, Cliente, Servicio, Trabajo
from openpyxl import Workbook
import io
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')  # fallback local
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


with app.app_context():
    db.create_all()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://"
    f"{os.environ.get('DB_USER', 'postgres')}:" +
    f"{os.environ.get('DB_PASS', 'postgres')}@" +
    f"{os.environ.get('DB_HOST', 'localhost')}:5432/" +
    f"{os.environ.get('DB_NAME', 'render')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.before_first_request
def crear_tablas():
    db.create_all()

# ---------- Clientes ----------
@app.post("/clientes")
def crear_cliente():
    data = request.json
    c = Cliente(**data)
    db.session.add(c); db.session.commit()
    return jsonify({"id": c.id})

@app.get("/clientes")
def listar_clientes():
    return jsonify([{"id": c.id, "nombre": c.nombre} for c in Cliente.query])

# ---------- Servicios ----------
@app.post("/servicios")
def crear_servicio():
    s = Servicio(**request.json)
    db.session.add(s); db.session.commit()
    return jsonify({"id": s.id})

@app.get("/servicios")
def listar_servicios():
    return jsonify([{"id": s.id, "tipo": s.tipo} for s in Servicio.query])

# ---------- Trabajos ----------
@app.post("/trabajos")
def crear_trabajo():
    t = Trabajo(**request.json)
    db.session.add(t); db.session.commit()
    return jsonify({"id": t.id, "proximo": t.proximo.isoformat()})

@app.get("/trabajos/<int:cliente_id>")
def trabajos_cliente(cliente_id):
    datos = [
        {
            "servicio": t.servicio.tipo,
            "fecha": t.fecha.isoformat(),
            "proximo": t.proximo.isoformat(),
            "comentarios": t.comentarios,
        }
        for t in Trabajo.query.filter_by(cliente_id=cliente_id)
    ]
    return jsonify(datos)

# ---------- Exportar Excel ----------
@app.get("/exportar/<int:cliente_id>")
def exportar_excel(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    wb, ws = Workbook(), None
    ws = wb.active; ws.title = "Trabajos"
    ws.append(["Servicio", "Fecha", "Próximo", "Comentarios"])
    for t in Trabajo.query.filter_by(cliente_id=cliente_id):
        ws.append([t.servicio.tipo, t.fecha, t.proximo, t.comentarios or ""])
    fp = io.BytesIO(); wb.save(fp); fp.seek(0)
    return send_file(fp, download_name=f"{cliente.nombre}.xlsx", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

