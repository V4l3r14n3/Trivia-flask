from flask import Flask, jsonify, render_template
from models import db, Pregunta
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///preguntas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pregunta/aleatoria")
def aleatoria():
    preguntas = Pregunta.query.all()
    if not preguntas:
        return jsonify({"error": "No hay preguntas"}), 404
    pregunta = random.choice(preguntas)
    opciones = [pregunta.opcion_1, pregunta.opcion_2, pregunta.opcion_3, pregunta.opcion_4]
    random.shuffle(opciones)  # Mezcla las opciones
    return jsonify({
        "id": pregunta.id,
        "pregunta": pregunta.pregunta,
        "categoria": pregunta.categoria,
        "opciones": opciones
    })


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
    with app.app_context():
        db.create_all()
        #crear_preguntas()
    app.run(debug=True)
