import json
from models import db, Pregunta
from app import app

def cargar_preguntas_desde_json():
    with open("preguntas.json", "r", encoding="utf-8") as f:
        datos = json.load(f)

    with app.app_context():
        db.drop_all()  # Limpia la base de datos por completo
        db.create_all()
        for item in datos:
            pregunta = Pregunta(
                pregunta=item["pregunta"],
                respuesta=item["respuesta"],
                categoria=item["categoria"],
                opcion_1=item["opcion_1"],
                opcion_2=item["opcion_2"],
                opcion_3=item["opcion_3"],
                opcion_4=item["opcion_4"]
            )
            db.session.add(pregunta)
        db.session.commit()
        print("Preguntas cargadas correctamente.")

if __name__ == "__main__":
    cargar_preguntas_desde_json()
