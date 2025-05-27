from flask import Flask, jsonify, render_template, request, session, redirect
from models import db, Pregunta
import random, json, unicodedata

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///preguntas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super-secret-key'
db.init_app(app)

# Función para quitar tildes y normalizar texto
def quitar_tildes(texto):
    if texto is None:
        return None
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

@app.route("/")
def menu():
    return render_template("menu.html")

@app.route("/jugar")
def jugar():
    session["categoria"] = request.args.get("categoria")
    session["dificultad"] = request.args.get("dificultad")
    session["vidas"] = 3
    return render_template("index.html")

@app.route("/pregunta/aleatoria")
def aleatoria():
    categoria = quitar_tildes(session.get("categoria", "").lower())
    dificultad = quitar_tildes(session.get("dificultad", "").lower())
    preguntas = Pregunta.query.filter_by(categoria=categoria, dificultad=dificultad).all()
    
    if not preguntas:
        return jsonify({"error": "No hay preguntas"}), 404

    pregunta = random.choice(preguntas)
    opciones = [pregunta.opcion_1, pregunta.opcion_2, pregunta.opcion_3, pregunta.opcion_4]
    opciones = [o for o in opciones if o is not None]
    random.shuffle(opciones)

    return jsonify({
        "id": pregunta.id,
        "pregunta": pregunta.pregunta,
        "categoria": pregunta.categoria,
        "opciones": opciones,
        "vidas": session.get("vidas", 3)
    })

@app.route("/respuesta/<int:id>")
def ver_respuesta(id):
    pregunta = Pregunta.query.get(id)
    if pregunta:
        return jsonify({"respuesta": pregunta.respuesta})
    return jsonify({"error": "No encontrada"}), 404

@app.route("/vidas/perder")
def perder_vida():
    vidas = session.get("vidas", 3)
    if vidas > 0:
        session["vidas"] = vidas - 1
    return jsonify({"vidas": session["vidas"]})

def cargar_preguntas_desde_json():
    with open("preguntas.json", "r", encoding="utf-8") as f:
        datos = json.load(f)
    
    for item in datos:
        existe = Pregunta.query.filter_by(pregunta=item["pregunta"]).first()
        if not existe:
            pregunta = Pregunta(
                pregunta=item["pregunta"],
                respuesta=item["respuesta"],
                categoria=quitar_tildes(item["categoria"].lower()),
                dificultad=quitar_tildes(item["dificultad"].lower()),
                opcion_1=item.get("opcion_1"),
                opcion_2=item.get("opcion_2"),
                opcion_3=item.get("opcion_3"),
                opcion_4=item.get("opcion_4")
            )
            db.session.add(pregunta)
    
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        cargar_preguntas_desde_json()  # Se ejecuta SIEMPRE, pero evita duplicados
    app.run(debug=True)
