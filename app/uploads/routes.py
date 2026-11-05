import os, uuid
from pathlib import Path, PurePosixPath
from flask import request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.config import Config
from app.extensions import db
from app.models import Analysis, SubmissionFile, AuditLog, SimilarityResult
from app.turmas.routes import get_owned_turma
from app.services.processing import sha256_file, process_file
from app.services.similarity.engine import compare_exact_hashes, classify_score
from . import uploads_bp

ALLOWED = {".dxf", ".dwg", ".pdf"}

@uploads_bp.post("/<int:analysis_id>")
@login_required
def upload(analysis_id):
    analysis = db.session.get(Analysis, analysis_id)
    if not analysis:
        abort(404)
    get_owned_turma(analysis.turma_id)
    uploaded = request.files.getlist("files")
    if not uploaded or len(uploaded) > Config.UPLOAD_MAX_FILES:
        flash("Selecione arquivos e respeite o limite configurado.", "danger")
        return redirect(url_for("analises.detalhe", analysis_id=analysis_id))
    base = Path(Config.STORAGE_PATH).resolve() / str(current_user.id) / str(analysis_id)
    base.mkdir(parents=True, exist_ok=True)
    accepted = 0
    for item in uploaded:
        raw = item.filename or ""
        # O caminho enviado pelo navegador é tratado apenas como metadado relativo.
        relative = PurePosixPath(raw.replace("\\", "/"))
        parts = [p for p in relative.parts if p not in ("", ".", "..", "/")]
        safe_relative = "/".join(parts[-8:]) or "arquivo"
        ext = Path(safe_relative).suffix.lower()
        if ext not in ALLOWED:
            continue
        internal_name = f"{uuid.uuid4().hex}{ext}"
        destination = (base / internal_name).resolve()
        if base not in destination.parents:
            continue
        item.save(destination)
        record = SubmissionFile(
            analysis_id=analysis_id, nome_original=Path(safe_relative).name[:255],
            caminho_relativo=safe_relative[:500],
            caminho_interno=str(destination), extensao=ext,
            tamanho=destination.stat().st_size, status="recebido"
        )
        db.session.add(record)
        db.session.flush()
        try:
            record.sha256 = sha256_file(destination)
            record.metadados = process_file(destination, ext, os.getenv("ODA_CONVERTER_PATH"))
            record.status = "processado"
        except Exception as exc:
            record.status = "nao_processado"
            record.erro = str(exc)[:2000]
        accepted += 1

    db.session.flush()
    for pair in compare_exact_hashes(analysis.arquivos):
        result = SimilarityResult(
            analysis_id=analysis_id, arquivo_a_id=pair["arquivo_a"].id,
            arquivo_b_id=pair["arquivo_b"].id, score_total=100,
            score_hash=100, evidencias=pair["evidencias"],
            classificacao=classify_score(100)
        )
        db.session.add(result)
    analysis.status = "concluida" if accepted else "sem_arquivos_validos"
    db.session.add(AuditLog(user_id=current_user.id, acao="upload",
        entidade="analysis", entidade_id=analysis_id,
        informacoes={"arquivos_recebidos": accepted}))
    db.session.commit()
    flash(f"{accepted} arquivo(s) recebido(s). Arquivos não processados aparecem com o motivo.", "success")
    return redirect(url_for("analises.detalhe", analysis_id=analysis_id))

