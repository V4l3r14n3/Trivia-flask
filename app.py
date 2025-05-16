from flask import Flask, jsonify, render_template
from models import db, Pregunta
import random
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///preguntas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def cargar_preguntas_desde_json():
    with open("preguntas.json", "r", encoding="utf-8") as f:
        datos = json.load(f)
    for item in datos:
        existe = Pregunta.query.filter_by(pregunta=item["pregunta"]).first()
        if not existe:
            pregunta = Pregunta(
                pregunta=item["pregunta"],
                respuesta=item["respuesta"],
                categoria=item["categoria"],
                opcion_1=item.get("opcion_1"),
                opcion_2=item.get("opcion_2"),
                opcion_3=item.get("opcion_3"),
                opcion_4=item.get("opcion_4")
            )
            db.session.add(pregunta)
    db.session.commit()

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
    opciones = [o for o in opciones if o is not None]  # eliminar None
    random.shuffle(opciones)
    return jsonify({
        "id": pregunta.id,
        "pregunta": pregunta.pregunta,
        "categoria": pregunta.categoria,
        "opciones": opciones
    })

@app.route("/respuesta/<int:id>")
def ver_respuesta(id):
    pregunta = Pregunta.query.get(id)
    if pregunta:
        return jsonify({"respuesta": pregunta.respuesta})
    return jsonify({"error": "No encontrada"}), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not Pregunta.query.first():
            cargar_preguntas_desde_json()
    app.run(debug=True)
