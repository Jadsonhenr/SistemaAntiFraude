from app.extensions import db
from app.models import User, Turma

def register(client, email="prof@furg.br"):
    return client.post("/cadastro", data={
        "nome": "Professor", "email": email, "senha": "senha-segura-123"
    }, follow_redirects=True)

def test_register_and_dashboard(client):
    response = register(client)
    assert response.status_code == 200
    assert b"Dashboard" in response.data

def test_password_is_hashed(app, client):
    register(client)
    user = db.session.query(User).filter_by(email="prof@furg.br").first()
    assert user.senha_hash != "senha-segura-123"
    assert user.check_password("senha-segura-123")

def test_user_cannot_access_other_teacher_class(app, client):
    register(client)
    with app.app_context():
        other = User(nome="Outro", email="outro@furg.br")
        other.set_password("outra-senha-segura")
        db.session.add(other)
        db.session.flush()
        turma = Turma(nome="Privada", disciplina="DT", professor_id=other.id)
        db.session.add(turma)
        db.session.commit()
        turma_id = turma.id
    response = client.get(f"/analises/nova/{turma_id}")
    assert response.status_code == 404
