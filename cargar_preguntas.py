import json
from models import db, Pregunta

def cargar_preguntas_desde_json(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        preguntas = json.load(archivo)
        for item in preguntas:
            pregunta = Pregunta(
                pregunta=item['pregunta'],
                respuesta=item['respuesta'],
                categoria=item['categoria'],
                dificultad=item['dificultad'],
                opcion_1=item['opcion_1'],
                opcion_2=item['opcion_2'],
                opcion_3=item['opcion_3'],
                opcion_4=item['opcion_4']
            )
            db.session.add(pregunta)
        db.session.commit()
