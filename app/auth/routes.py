from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from sqlalchemy import func
from app.extensions import db
from app.models import User
from . import auth_bp

@auth_bp.route("/cadastro", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        if not nome or not email or len(senha) < 10:
            flash("Informe nome, e-mail e senha com pelo menos 10 caracteres.", "danger")
        elif db.session.scalar(db.select(User).where(func.lower(User.email) == email)):
            flash("Este e-mail já está cadastrado.", "danger")
        else:
            user = User(nome=nome, email=email)
            user.set_password(senha)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("dashboard.index"))
    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        user = db.session.scalar(db.select(User).where(func.lower(User.email) == email))
        if user and user.check_password(senha):
            login_user(user)
            return redirect(url_for("dashboard.index"))
        flash("E-mail ou senha inválidos.", "danger")
    return render_template("auth/login.html")

@auth_bp.post("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
