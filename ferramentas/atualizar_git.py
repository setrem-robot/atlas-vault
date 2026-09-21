"""Registra todas as branches, alterações e commits locais sem mudar código.

Uso: python ferramentas/atualizar_git.py [--fetch]
Sem --fetch, a comparação usa apenas as referências remotas já conhecidas.
O resultado é um novo snapshot; as notas narrativas exigem revisão humana.
"""
from pathlib import Path
from datetime import datetime
import argparse
import json
import subprocess
import sys

VAULT = Path(__file__).resolve().parents[1]
ROOT = VAULT.parent

def git(repo, *args, required=True):
    proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, encoding="utf-8")
    if required and proc.returncode:
        raise RuntimeError(f"git {args[0]} falhou em {repo.name}: {proc.stderr}")
    return proc.stdout.strip() if proc.returncode == 0 else None

def commits(repo, *revision):
    raw = git(repo, "log", "--date=iso-strict", "--format=%H%x09%aI%x09%cI%x09%s", *revision)
    return [dict(zip(["sha", "data_autoria", "data_commit", "assunto"], line.split("\t", 3))) for line in raw.splitlines()]

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()
    now = datetime.now().astimezone()
    stamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    report = {"coletado_em": now.isoformat(), "fetch_solicitado": args.fetch, "repositorios": []}
    for name, remote in [("app", "aplicativo"), ("orquestrador", "orquestrador"), ("RobotEye", "atlas_ai_v2")]:
        repo = ROOT / name
        result = {"pasta": name, "github": f"https://github.com/setrem-robot/{remote}"}
        result["fetch_ok"] = git(repo, "fetch", "origin", required=False) is not None if args.fetch else None
        result["head"] = git(repo, "rev-parse", "HEAD")
        result["branch"] = git(repo, "branch", "--show-current")
        result["status"] = git(repo, "status", "--porcelain=v1", "--untracked-files=all")
        result["alteracoes_resumo"] = git(repo, "diff", "--stat", "HEAD")
        result["commits_locais_nao_alcancaveis_por_remotos"] = commits(repo, "--branches", "--not", "--remotes")
        result["historico_todas_branches"] = commits(repo, "--all")
        result["branches"] = []
        rows = git(repo, "for-each-ref", "--format=%(refname:short)%09%(objectname)%09%(upstream:short)", "refs/heads")
        for row in rows.splitlines():
            fields = row.split("\t")
            branch, sha = fields[:2]
            upstream = fields[2] if len(fields) > 2 else ""
            b = {"nome": branch, "sha": sha, "upstream": upstream, "comparacao_upstream": None}
            if upstream:
                count = git(repo, "rev-list", "--left-right", "--count", f"{branch}...{upstream}", required=False)
                b["comparacao_upstream"] = dict(zip(["a_frente", "atras"], map(int, count.split()))) if count else "referencia_ausente"
            count = git(repo, "rev-list", "--left-right", "--count", f"{branch}...origin/main", required=False)
            b["comparacao_main"] = dict(zip(["exclusivos_branch", "exclusivos_main"], map(int, count.split()))) if count else None
            b["nao_alcancaveis_por_remotos"] = commits(repo, branch, "--not", "--remotes")
            result["branches"].append(b)
        report["repositorios"].append(result)
    out = VAULT / "fontes" / "auditoria"
    out.mkdir(parents=True, exist_ok=True)
    target = out / f"git-{stamp}.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [f"# Retrato Git — {now.strftime('%d/%m/%Y %H:%M:%S %z')}", "", "[[wiki/estado/git-local-e-remoto|Como interpretar e usar esta coleta]]", "", f"Consulta remota nesta execução: {'solicitada; veja resultado por repo' if args.fetch else 'não; referências podem estar desatualizadas'}.", "", f"Detalhes: [[{target.relative_to(VAULT).as_posix()}|JSON da coleta]].", ""]
    for r in report["repositorios"]:
        lines += [f"## {r['pasta']}", "", f"Branch: `{r['branch']}` · HEAD: `{r['head']}` · fetch: `{r['fetch_ok']}`.", "", f"Árvore de trabalho: {'há alterações, veja abaixo' if r['status'] else 'limpa'}.", "", f"Commits em branches locais sem alcance por qualquer referência remota conhecida: **{len(r['commits_locais_nao_alcancaveis_por_remotos'])}**.", "", "| Branch | SHA | Upstream | À frente / atrás | Exclusivos ante main |", "|---|---|---|---|---|"]
        for b in r["branches"]:
            comp = b["comparacao_upstream"]
            label = f"{comp['a_frente']} / {comp['atras']}" if isinstance(comp, dict) else str(comp or "sem upstream")
            delta = b["comparacao_main"]
            lines.append(f"| `{b['nome']}` | `{b['sha'][:7]}` | `{b['upstream'] or '—'}` | {label} | {delta['exclusivos_branch'] if delta else 'não disponível'} |")
        if r["status"]:
            lines += ["", "```text", r["status"], "```"]
        for c in r["commits_locais_nao_alcancaveis_por_remotos"]:
            lines += ["", f"- `{c['sha'][:7]}` — {c['assunto']}"]
        lines += [""]
    lines += ["## Limites", "", "Uma branch cujo upstream sumiu pode já ter sido integrada ou publicada em outra branch. Commits exclusivos ante main também podem estar publicados em produção ou em branches de trabalho. A classificação usa alcance no grafo Git; integrações por squash podem ter conteúdo equivalente com SHA diferente. Não há inspeção da versão instalada no Raspberry Pi nem da VM."]
    note = VAULT / "wiki" / "estado" / "coletas" / f"git-{stamp}.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(note)
    for r in report["repositorios"]:
        print(r["pasta"], r["branch"], r["head"][:7], "locais:", len(r["commits_locais_nao_alcancaveis_por_remotos"]), "alterações:", bool(r["status"]))

if __name__ == "__main__":
    main()
