from datetime import datetime, timezone
from app.extensions import db

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    disciplina = db.Column(db.String(160), nullable=False)
    descricao = db.Column(db.Text)
    professor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    criado_em = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    professor = db.relationship("User", back_populates="turmas")
    analises = db.relationship("Analysis", back_populates="turma", cascade="all, delete-orphan")
