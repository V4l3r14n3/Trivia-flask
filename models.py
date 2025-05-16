# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pregunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pregunta = db.Column(db.String(200), nullable=False)
    respuesta = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
