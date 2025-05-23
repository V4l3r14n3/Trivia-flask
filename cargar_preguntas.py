import json
from models import db, Pregunta
from app import app  # Asegúrate de que el archivo app.py define el objeto `app`

def cargar_preguntas_desde_json(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            preguntas = json.load(archivo)
            nuevas = 0
            for item in preguntas:
                existe = Pregunta.query.filter_by(pregunta=item['pregunta']).first()
                if existe:
                    print(f"❌ Pregunta duplicada ignorada: {item['pregunta']}")
                    continue
                pregunta = Pregunta(
                    pregunta=item['pregunta'],
                    respuesta=item['respuesta'],
                    categoria=item['categoria'],
                    dificultad=item['dificultad'],
                    opcion_1=item.get('opcion_1'),
                    opcion_2=item.get('opcion_2'),
                    opcion_3=item.get('opcion_3'),
                    opcion_4=item.get('opcion_4')
                )
                db.session.add(pregunta)
                nuevas += 1
            db.session.commit()
            total = Pregunta.query.count()
            print(f"✅ Se cargaron {nuevas} nuevas preguntas desde '{nombre_archivo}'.")
            print(f"📊 Total de preguntas en la base de datos: {total}")
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{nombre_archivo}'.")
    except json.JSONDecodeError:
        print(f"❌ Error: El archivo '{nombre_archivo}' no tiene un formato JSON válido.")
    except Exception as e:
        print(f"❌ Error inesperado al cargar preguntas: {e}")

if __name__ == "__main__":
    with app.app_context():
        cargar_preguntas_desde_json("preguntas.json")
