#!/usr/bin/env python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class Cliente(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    nombre      = db.Column(db.String(120), nullable=False)
    telefono    = db.Column(db.String(50))
    direccion   = db.Column(db.String(200))
    correo      = db.Column(db.String(120))

class Servicio(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    tipo        = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.String(250))
    precio      = db.Column(db.Numeric(10,2))

class Trabajo(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    cliente_id  = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicio.id'), nullable=False)
    fecha       = db.Column(db.Date, default=datetime.utcnow)
    comentarios = db.Column(db.Text)
    evidencia   = db.Column(db.Text)
    proximo     = db.Column(db.Date)

    cliente     = db.relationship('Cliente')
    servicio    = db.relationship('Servicio')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # seguimiento a 90 días
        self.proximo = self.fecha + timedelta(days=90)
