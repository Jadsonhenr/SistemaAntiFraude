from datetime import datetime, timezone
from app.extensions import db

class SimilarityResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey("analysis.id"), nullable=False, index=True)
    arquivo_a_id = db.Column(db.Integer, db.ForeignKey("submission_file.id"), nullable=False)
    arquivo_b_id = db.Column(db.Integer, db.ForeignKey("submission_file.id"), nullable=False)
    score_total = db.Column(db.Float, nullable=False)
    score_hash = db.Column(db.Float)
    score_estrutural = db.Column(db.Float)
    score_geometrico = db.Column(db.Float)
    score_visual = db.Column(db.Float)
    score_textual = db.Column(db.Float)
    evidencias = db.Column(db.JSON)
    classificacao = db.Column(db.String(40), nullable=False)
    criado_em = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    analise = db.relationship("Analysis", back_populates="resultados")
    arquivo_a = db.relationship("SubmissionFile", foreign_keys=[arquivo_a_id])
    arquivo_b = db.relationship("SubmissionFile", foreign_keys=[arquivo_b_id])

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    acao = db.Column(db.String(100), nullable=False)
    entidade = db.Column(db.String(80), nullable=False)
    entidade_id = db.Column(db.Integer)
    criado_em = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    informacoes = db.Column(db.JSON)
