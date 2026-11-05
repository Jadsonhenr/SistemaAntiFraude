from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from sqlalchemy import select
from app.extensions import db
from app.models import Analysis
from app.turmas.routes import get_owned_turma
from . import analises_bp

@analises_bp.route("/nova/<int:turma_id>", methods=["GET", "POST"])
@login_required
def nova(turma_id):
    turma = get_owned_turma(turma_id)
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        if not nome:
            flash("Informe o nome da atividade.", "danger")
        else:
            analise = Analysis(turma_id=turma.id, nome=nome,
                               descricao=request.form.get("descricao", "").strip())
            db.session.add(analise)
            db.session.commit()
            return redirect(url_for("analises.detalhe", analysis_id=analise.id))
    return render_template("analises/form.html", turma=turma)

@analises_bp.get("/<int:analysis_id>")
@login_required
def detalhe(analysis_id):
    analise = db.session.get(Analysis, analysis_id)
    if not analise:
        abort(404)
    get_owned_turma(analise.turma_id)
    return render_template("analises/detail.html", analise=analise)
