from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from sqlalchemy import select
from app.extensions import db
from app.models import Turma
from . import turmas_bp

@turmas_bp.get("/")
@login_required
def index():
    turmas = db.session.scalars(select(Turma).where(Turma.professor_id == current_user.id).order_by(Turma.nome)).all()
    return render_template("turmas/index.html", turmas=turmas)

@turmas_bp.route("/nova", methods=["GET", "POST"])
@login_required
def nova():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        disciplina = request.form.get("disciplina", "").strip()
        if not nome or not disciplina:
            flash("Nome e disciplina são obrigatórios.", "danger")
        else:
            turma = Turma(nome=nome, disciplina=disciplina,
                          descricao=request.form.get("descricao", "").strip(),
                          professor_id=current_user.id)
            db.session.add(turma)
            db.session.commit()
            flash("Turma criada.", "success")
            return redirect(url_for("turmas.index"))
    return render_template("turmas/form.html")

def get_owned_turma(turma_id):
    turma = db.session.get(Turma, turma_id)
    if not turma or turma.professor_id != current_user.id:
        abort(404)
    return turma
