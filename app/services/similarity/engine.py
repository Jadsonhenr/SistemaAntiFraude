def classify_score(score):
    if score >= 100: return "Idêntica"
    if score >= 90: return "Extremamente alta"
    if score >= 75: return "Alta"
    if score >= 50: return "Moderada"
    if score >= 25: return "Baixa"
    return "Pouca similaridade"

def compare_exact_hashes(files):
    """Retorna pares binariamente idênticos. Não infere similaridade visual."""
    groups = {}
    for item in files:
        if item.sha256 and item.status == "processado":
            groups.setdefault(item.sha256, []).append(item)
    pairs = []
    for digest, group in groups.items():
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                pairs.append({
                    "arquivo_a": group[i], "arquivo_b": group[j],
                    "score": 100.0, "evidencias": {
                        "metodo": "SHA-256", "hash": digest,
                        "interpretacao": "Arquivos binariamente idênticos."
                    }
                })
    return pairs
