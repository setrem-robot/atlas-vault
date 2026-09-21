"""Coleta documental inicial; não altera os repositórios de software."""
from pathlib import Path
import base64
import hashlib
import json
import subprocess
import sys
import zipfile
import pymupdf

sys.stdout.reconfigure(encoding="utf-8")
VAULT = Path(__file__).resolve().parents[1]
ROOT = VAULT.parent
OUT = VAULT / "fontes"

def gh(endpoint):
    proc = subprocess.run(["gh", "api", endpoint], capture_output=True, encoding="utf-8", check=True)
    return json.loads(proc.stdout)

def main():
    manifest = []
    for source in (ROOT / "Relatorios").glob("*.pdf"):
        target = OUT / "relatorios" / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        doc = pymupdf.open(source)
        target.with_suffix(".txt").write_text("\n\n".join(f"## Página {i+1}\n\n{page.get_text()}" for i, page in enumerate(doc)), encoding="utf-8")
        manifest.append({"origem": str(source), "copia": target.relative_to(VAULT).as_posix(), "paginas": len(doc), "sha256": hashlib.sha256(source.read_bytes()).hexdigest()})
    for name in ["app", "orquestrador", "RobotEye"]:
        repo = ROOT / name
        paths = subprocess.run(["git", "-C", str(repo), "ls-files", "-z"], capture_output=True, check=True).stdout.decode("utf-8").split("\0")
        with zipfile.ZipFile(OUT / f"codigo-{name}-2026-09-09.zip", "w", zipfile.ZIP_DEFLATED) as z:
            for rel in paths:
                if not rel:
                    continue
                source = repo / rel
                # Somente arquivos rastreados. Credenciais reais e ambientes ficam fora.
                if not source.is_file() or source.suffix in {".jks", ".pem", ".key"} or source.name in {".env", "key.properties", "bridge.conf"}:
                    continue
                z.write(source, rel)
                manifest.append({"origem": f"{name}/{rel}", "arquivo_zip": f"codigo-{name}-2026-09-09.zip", "sha256": hashlib.sha256(source.read_bytes()).hexdigest()})
    for repo, branch, wanted in [
        ("doc-interdisciplinar-4-semestre", "master", ["main.tex", "main.pdf", "tex/intro.tex", "tex/cap1.tex", "tex/cap2.tex", "tex/cap3.tex", "tex/conclusao.tex"]),
        (".github", "main", ["profile/README.md"]),
    ]:
        head = gh(f"repos/setrem-robot/{repo}/commits/{branch}")["sha"]
        dst = OUT / "github" / repo
        dst.mkdir(parents=True, exist_ok=True)
        (dst / "referencia.json").write_text(json.dumps({"repo": repo, "branch": branch, "sha": head}, indent=2), encoding="utf-8")
        for rel in wanted:
            data = gh(f"repos/setrem-robot/{repo}/contents/{rel}?ref={head}")
            content = base64.b64decode(data["content"])
            target = dst / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            manifest.append({"origem": f"https://github.com/setrem-robot/{repo}/blob/{head}/{rel}", "copia": target.relative_to(VAULT).as_posix(), "sha256": hashlib.sha256(content).hexdigest()})
            if target.suffix == ".pdf":
                doc = pymupdf.open(target)
                target.with_suffix(".txt").write_text("\n\n".join(f"## Página {i+1}\n\n{page.get_text()}" for i, page in enumerate(doc)), encoding="utf-8")
        history = gh(f"repos/setrem-robot/{repo}/commits?sha={head}&per_page=100")
        (dst / "commits.json").write_text(json.dumps([{"sha": x["sha"], "data": x["commit"]["committer"]["date"], "mensagem": x["commit"]["message"]} for x in history], ensure_ascii=False, indent=2), encoding="utf-8")
        print(repo, head)
    (OUT / "auditoria" / "manifesto-fontes.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(manifest)} arquivos no manifesto")

if __name__ == "__main__":
    main()
