from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pregunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pregunta = db.Column(db.String, unique=True, nullable=False)
    respuesta = db.Column(db.String, nullable=False)
    categoria = db.Column(db.String, nullable=False)
    dificultad = db.Column(db.String, nullable=False)
    opcion_1 = db.Column(db.String)
    opcion_2 = db.Column(db.String)
    opcion_3 = db.Column(db.String)
    opcion_4 = db.Column(db.String)
