from app import app
from models import db, Pregunta
import unicodedata

def quitar_tildes(texto):
    if texto is None:
        return None
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

with app.app_context():
    preguntas = Pregunta.query.all()
    for p in preguntas:
        p.categoria = quitar_tildes(p.categoria.lower())
        p.dificultad = quitar_tildes(p.dificultad.lower())
    db.session.commit()
    print("✅ Preguntas normalizadas correctamente.")
