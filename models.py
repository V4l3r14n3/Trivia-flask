id = db.Column(db.Integer, primary_key=True)
texto = db.Column(db.String(255), nullable=False)
opcion_a = db.Column(db.String(100), nullable=False)
opcion_b = db.Column(db.String(100), nullable=False)
opcion_c = db.Column(db.String(100), nullable=False)
opcion_d = db.Column(db.String(100), nullable=False)
respuesta_correcta = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C' o 'D'
categoria = db.Column(db.String(50), nullable=False)  # Ciencia, Historia, etc.
dificultad = db.Column(db.String(20), nullable=False)  # Fácil, Media, Difícil

def to_dict(self):
    return {
        "id": self.id,
        "texto": self.texto,
        "opciones": {
            "A": self.opcion_a,
            "B": self.opcion_b,
            "C": self.opcion_c,
            "D": self.opcion_d
        },
        "categoria": self.categoria,
        "dificultad": self.dificultad
    }
