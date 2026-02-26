# src/colab_bootstrap.py
from __future__ import annotations

import os
import sys
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class RepoConfig:
    github_repo: str = "https://github.com/sergiocostaifes/PPCOMP_DM.git"
    base_dir: str = "/content/drive/MyDrive/Mestrado"
    repo_name: str = "PPCOMP_DM"
    force_remount_drive: bool = True
    auto_pull: bool = True  # só puxa se working tree estiver limpo
    verbose: bool = True


def _run(cmd: list[str], cwd: Optional[str] = None, check: bool = True) -> str:
    if cmd and isinstance(cmd[0], str) and cmd[0] == "git":
        # evita prompts interativos no Colab
        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = "0"
    else:
        env = None

    if cwd is None:
        p = subprocess.run(cmd, text=True, capture_output=True, env=env)
    else:
        p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, env=env)

    out = (p.stdout or "").strip()
    err = (p.stderr or "").strip()

    if check and p.returncode != 0:
        msg = f"Falha ao executar: {' '.join(cmd)}\nSTDOUT:\n{out}\nSTDERR:\n{err}"
        raise RuntimeError(msg)

    # mantém o erro disponível para debug, sem quebrar
    if p.returncode != 0 and err:
        out = out + ("\n" if out else "") + err

    return out


def _git_working_tree_clean(repo_dir: Path) -> bool:
    # --porcelain é estável para scripts
    out = _run(["git", "status", "--porcelain"], cwd=str(repo_dir), check=True)
    return len(out.strip()) == 0


def ensure_repo_ready(config: RepoConfig = RepoConfig()) -> Path:
    """
    Garante que:
      - Drive está montado
      - Repo existe em base_dir/repo_name (clone inicial se faltar)
      - Repo é atualizado via git pull SOMENTE se working tree estiver limpo
      - Repo é adicionado ao sys.path
      - src/__init__.py existe (para imports)
    Retorna o Path do diretório do repositório.
    """
    # 1) Montar Drive (Colab)
    from google.colab import drive  # type: ignore

    drive.mount("/content/drive", force_remount=config.force_remount_drive)

    base_dir = Path(config.base_dir)
    repo_dir = base_dir / config.repo_name
    base_dir.mkdir(parents=True, exist_ok=True)

    def vprint(*args):
        if config.verbose:
            print(*args)

    # 2) Clone inicial ou validação
    if not repo_dir.exists():
        vprint(f"[BOOTSTRAP] Repo não encontrado. Clonando em: {repo_dir}")
        _run(["git", "clone", config.github_repo, str(repo_dir)], check=True)
    else:
        # Confere se é git repo
        if not (repo_dir / ".git").exists():
            raise RuntimeError(
                f"[BOOTSTRAP] {repo_dir} existe, mas não parece ser um repositório Git (faltou .git)."
            )

        # 3) Pull só se working tree estiver limpo
        if config.auto_pull:
            clean = _git_working_tree_clean(repo_dir)
            if clean:
                vprint("[BOOTSTRAP] Working tree limpo. Executando git pull...")
                pull_out = _run(["git", "pull"], cwd=str(repo_dir), check=False)
                vprint("[BOOTSTRAP] git pull output:\n", pull_out)
            else:
                vprint(
                    "[BOOTSTRAP] ATENÇÃO: há alterações locais não commitadas.\n"
                    "           Não vou executar git pull para evitar conflitos.\n"
                    "           Rode: git status / git add / git commit, ou descarte mudanças."
                )

    # 4) Garantir src como pacote
    src_dir = repo_dir / "src"
    src_dir.mkdir(parents=True, exist_ok=True)
    init_file = src_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text("# src package\n", encoding="utf-8")
        vprint("[BOOTSTRAP] Criado src/__init__.py (não commitado automaticamente).")

    # 5) sys.path
    if str(repo_dir) not in sys.path:
        sys.path.append(str(repo_dir))

    vprint("[BOOTSTRAP] Repo pronto:", repo_dir)
    return repo_dir
