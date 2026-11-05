from flask import render_template, abort
from flask_login import login_required, current_user
from sqlalchemy import select
from app.extensions import db
from app.models import Analysis, SimilarityResult
from app.turmas.routes import get_owned_turma
from . import reports_bp

@reports_bp.get("/<int:analysis_id>")
@login_required
def index(analysis_id):
    analysis = db.session.get(Analysis, analysis_id)
    if not analysis:
        abort(404)
    get_owned_turma(analysis.turma_id)
    results = db.session.scalars(select(SimilarityResult).where(
        SimilarityResult.analysis_id == analysis_id
    ).order_by(SimilarityResult.score_total.desc())).all()
    return render_template("reports/index.html", analysis=analysis, results=results)
