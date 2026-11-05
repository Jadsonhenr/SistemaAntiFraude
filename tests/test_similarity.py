from types import SimpleNamespace
from app.services.similarity.engine import compare_exact_hashes, classify_score

def test_exact_hash_match():
    a = SimpleNamespace(sha256="abc", status="processado", id=1)
    b = SimpleNamespace(sha256="abc", status="processado", id=2)
    assert len(compare_exact_hashes([a,b])) == 1
    assert classify_score(100) == "Idêntica"

def test_different_hashes_do_not_match():
    a = SimpleNamespace(sha256="abc", status="processado", id=1)
    b = SimpleNamespace(sha256="def", status="processado", id=2)
    assert compare_exact_hashes([a,b]) == []
