from flask import Flask, jsonify, render_template
from models import db, Pregunta
import random
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///preguntas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Crear preguntas si no existen
def crear_preguntas():
    if Pregunta.query.first():
        return
    ejemplo = [
        Pregunta(pregunta="¿Cuál es la capital de Francia?", respuesta="París", categoria="Geografía"),
        Pregunta(pregunta="¿Cuánto es 8 x 7?", respuesta="56", categoria="Matemáticas")
    ]
    db.session.add_all(ejemplo)
    db.session.commit()

@app.before_first_request
def setup():
    db.create_all()
    crear_preguntas()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pregunta/aleatoria")
def aleatoria():
    preguntas = Pregunta.query.all()
    if not preguntas:
        return jsonify({"error": "No hay preguntas"}), 404
    pregunta = random.choice(preguntas)
    return jsonify({"id": pregunta.id, "pregunta": pregunta.pregunta, "categoria": pregunta.categoria})

@app.route("/preguntas/categoria/<categoria>")
def por_categoria(categoria):
    preguntas = Pregunta.query.filter_by(categoria=categoria).all()
    return jsonify([{"id": p.id, "pregunta": p.pregunta} for p in preguntas])

@app.route("/respuesta/<int:id>")
def ver_respuesta(id):
    pregunta = Pregunta.query.get(id)
    if pregunta:
        return jsonify({"respuesta": pregunta.respuesta})
    return jsonify({"error": "No encontrada"}), 404

if __name__ == "__main__":
    app.run(debug=True)
