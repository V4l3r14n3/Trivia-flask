from flask import Flask, jsonify, render_template
import random
import json

app = Flask(__name__)

# Cargar preguntas
with open('preguntas.json', 'r', encoding='utf-8') as f:
    preguntas = json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pregunta/aleatoria")
def pregunta_aleatoria():
    return jsonify(random.choice(preguntas))

@app.route("/preguntas/categoria/<categoria>")
def por_categoria(categoria):
    filtradas = [p for p in preguntas if p["categoria"].lower() == categoria.lower()]
    return jsonify(filtradas)

@app.route("/respuesta/<int:id>")
def ver_respuesta(id):
    p = next((p for p in preguntas if p["id"] == id), None)
    return jsonify({"respuesta": p["respuesta"]}) if p else ("No encontrada", 404)

if __name__ == "__main__":
    app.run(debug=True)