from datetime import datetime, timezone
from app.extensions import db

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turma_id = db.Column(db.Integer, db.ForeignKey("turma.id"), nullable=False, index=True)
    nome = db.Column(db.String(180), nullable=False)
    descricao = db.Column(db.Text)
    status = db.Column(db.String(30), nullable=False, default="aguardando_upload")
    criado_em = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    concluido_em = db.Column(db.DateTime(timezone=True))
    resumo = db.Column(db.JSON)

    turma = db.relationship("Turma", back_populates="analises")
    arquivos = db.relationship("SubmissionFile", back_populates="analise", cascade="all, delete-orphan")
    resultados = db.relationship("SimilarityResult", back_populates="analise", cascade="all, delete-orphan")

class SubmissionFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey("analysis.id"), nullable=False, index=True)
    nome_original = db.Column(db.String(255), nullable=False)
    caminho_relativo = db.Column(db.String(500), nullable=False)
    caminho_interno = db.Column(db.String(700), nullable=False, unique=True)
    extensao = db.Column(db.String(20), nullable=False)
    tamanho = db.Column(db.BigInteger, nullable=False)
    sha256 = db.Column(db.String(64), index=True)
    status = db.Column(db.String(30), nullable=False, default="recebido")
    erro = db.Column(db.Text)
    metadados = db.Column(db.JSON)

    analise = db.relationship("Analysis", back_populates="arquivos")
