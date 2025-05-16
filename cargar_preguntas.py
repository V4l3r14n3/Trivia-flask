import json
from app import app, db, Pregunta

with app.app_context():
    with open('preguntas.json', 'r', encoding='utf-8') as f:
        datos = json.load(f)

    for item in datos:
        pregunta = Pregunta(
            pregunta=item["pregunta"],
            respuesta=item["respuesta"],
            categoria=item["categoria"]
        )
        db.session.add(pregunta)

    db.session.commit()
    print("Preguntas cargadas exitosamente.")
