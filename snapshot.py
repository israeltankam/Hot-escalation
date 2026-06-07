import os
import hashlib
from pathlib import Path

# dossier du site à analyser
ROOT_DIR = Path(".")  # mettre le chemin si besoin

# dossiers dont on veut montrer l'existence sans en exposer le contenu
HIDDEN_DIRS = {"venv", ".streamlit"}

# dossiers à ignorer complètement
SKIP_DIRS = {".git"}

# extensions considérées comme texte (modifiables)
TEXT_EXTENSIONS = {
    ".html", ".htm", ".md", ".css", ".js",
    ".toml", ".yaml", ".yml", ".json",
    ".txt", ".xml", ".py", ".db", ".sql"
}

# extensions à ignorer complètement dans la section "Contenu"
IGNORE_EXTENSIONS = {".png", ".svg", ".jpg", ".jpeg", ".gif", ".webp"}

OUTPUT_FILE = "app_snapshot.md"


def file_hash(path: Path) -> str:
    """Calcule le hash SHA256 d'un fichier."""
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS


def should_skip_path(path: Path) -> bool:
    """Retourne True si le chemin doit être totalement ignoré."""
    return any(part in SKIP_DIRS for part in path.parts)


def is_inside_hidden_dir(path: Path) -> bool:
    """Retourne True si le chemin est dans un dossier dont on masque le contenu."""
    return any(part in HIDDEN_DIRS for part in path.parts)


def write_tree(out, directory: Path, level: int = 0):
    """Écrit l'arborescence en affichant les dossiers masqués sans descendre dedans."""
    if should_skip_path(directory):
        return

    indent = "  " * level
    name = directory.name if level > 0 else directory.resolve().name
    out.write(f"{indent}{name}/\n")

    try:
        entries = sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    except PermissionError:
        out.write(f"{indent}  [accès refusé]\n")
        return

    for entry in entries:
        if should_skip_path(entry):
            continue

        if entry.is_dir():
            if entry.name in HIDDEN_DIRS:
                out.write(f"{indent}  {entry.name}/ [contenu masqué]\n")
            else:
                write_tree(out, entry, level + 1)
        else:
            out.write(f"{indent}  {entry.name}\n")


with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write("# Snapshot complet du site\n\n")
    out.write(f"Racine analysée : {ROOT_DIR.resolve()}\n\n")

    # 1. Arborescence
    out.write("## Arborescence\n\n")
    write_tree(out, ROOT_DIR)

    out.write("\n---\n")

    # 2. Contenu des fichiers
    out.write("## Contenu\n\n")

    for path in ROOT_DIR.rglob("*"):
        # Ignorer les chemins dans .git, venv, .streamlit, etc.
        if should_skip_path(path) or is_inside_hidden_dir(path):
            continue

        if path.is_dir():
            continue

        # Ignorer complètement les fichiers image
        if path.suffix.lower() in IGNORE_EXTENSIONS:
            continue

        out.write(f"\n# FILE: {path}\n")

        if is_text_file(path):
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                content = path.read_text(errors="ignore")

            lang = path.suffix.lstrip(".")
            out.write(f"```{lang}\n")
            out.write(content)
            out.write("\n```\n")
        else:
            size = path.stat().st_size
            h = file_hash(path)

            out.write("Binary file\n")
            out.write(f"Size: {size} bytes\n")
            out.write(f"SHA256: {h}\n")

print(f"Snapshot créé : {OUTPUT_FILE}")