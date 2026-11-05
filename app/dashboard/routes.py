from flask import render_template
from flask_login import login_required, current_user
from sqlalchemy import select, func
from app.extensions import db
from app.models import Turma, Analysis, SubmissionFile, SimilarityResult
from . import dashboard_bp

@dashboard_bp.get("/")
@login_required
def index():
    turmas = db.session.scalar(select(func.count(Turma.id)).where(Turma.professor_id == current_user.id)) or 0
    analysis_ids = select(Analysis.id).join(Turma).where(Turma.professor_id == current_user.id)
    analises = db.session.scalar(select(func.count(Analysis.id)).join(Turma).where(Turma.professor_id == current_user.id)) or 0
    arquivos = db.session.scalar(select(func.count(SubmissionFile.id)).where(SubmissionFile.analysis_id.in_(analysis_ids))) or 0
    pares = db.session.scalar(select(func.count(SimilarityResult.id)).where(
        SimilarityResult.analysis_id.in_(analysis_ids), SimilarityResult.score_total >= 75
    )) or 0
    recentes = db.session.scalars(select(Analysis).join(Turma).where(
        Turma.professor_id == current_user.id
    ).order_by(Analysis.criado_em.desc()).limit(5)).all()
    return render_template("dashboard/index.html", turmas=turmas, analises=analises,
                           arquivos=arquivos, pares=pares, recentes=recentes)
