import hashlib
from pathlib import Path
import fitz
import ezdxf

SUPPORTED = {".dxf", ".dwg", ".pdf"}

def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def process_file(path, extension, oda_converter=None):
    ext = extension.lower()
    metadata = {}
    if ext == ".dxf":
        doc = ezdxf.readfile(path)
        modelspace = doc.modelspace()
        counts = {}
        for entity in modelspace:
            counts[entity.dxftype()] = counts.get(entity.dxftype(), 0) + 1
        metadata = {"tipo": "DXF", "quantidade_entidades": len(modelspace),
                    "tipos_entidades": counts, "layers": [layer.dxf.name for layer in doc.layers]}
    elif ext == ".pdf":
        with fitz.open(path) as doc:
            metadata = {"tipo": "PDF", "paginas": len(doc),
                        "texto_por_pagina": [page.get_text()[:20000] for page in doc]}
    elif ext == ".dwg":
        if not oda_converter or not Path(oda_converter).exists():
            raise RuntimeError("DWG não processado: ODA File Converter não configurado/disponível.")
        raise RuntimeError("Adaptador ODA ainda precisa ser configurado para esta instalação.")
    else:
        raise RuntimeError(f"Formato não suportado: {ext}")
    return metadata
