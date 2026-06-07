# Snapshot complet du site

Racine analysée : C:\Users\tankamch\Desktop\Hot Escalation

## Arborescence

Hot Escalation/
  .streamlit/ [contenu masqué]
  assets/
    sounds/
      success.mp3
    style.css
  data/
    gages.json
  scripts/
    generate_json.py
    reorganize_json.py
  utils/
    __pycache__/
      engine.cpython-312.pyc
      engine.cpython-314.pyc
      state.cpython-312.pyc
      state.cpython-314.pyc
    __init__.py
    engine.py
    state.py
  venv/ [contenu masqué]
  .gitignore
  app.py
  app_snapshot.md
  requirements.txt
  snapshot.py

---
## Contenu


# FILE: .gitignore
Binary file
Size: 324 bytes
SHA256: ecbf16d3189cc3d7d53ed5c1e177b12c4632bc21378a0623b258b921eeffc366

# FILE: app.py
```py
import streamlit as st
import time
import random
from utils.engine import GameEngine
from utils.state import init_state, get_elapsed_time, get_progress

st.set_page_config(page_title="Hot Escalation", page_icon="🔥", layout="centered")

# Load CSS
with open("assets/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

init_state()
engine = GameEngine()

def next_turn():
    st.session_state.history.append(st.session_state.current_gage['id'])
    st.session_state.next_player = "Femme" if st.session_state.next_player == "Homme" else "Homme"
    st.session_state.drink_counter += 1
    st.session_state.gages_in_current_phase += 1
    st.session_state.total_done += 1
    
    # Logic pour changement de phase automatique basé sur le ratio 5, 4, 3, 2, 1
    target_for_current_phase = st.session_state.phase_distribution.get(st.session_state.current_phase, 1)
    
    if st.session_state.gages_in_current_phase >= target_for_current_phase:
        if st.session_state.current_phase < 5:
            if st.session_state.current_phase == 4 and not st.session_state.sex_finality:
                pass # Rester en phase 4 si pas de finalité sexe
            else:
                st.session_state.current_phase += 1
                st.session_state.gages_in_current_phase = 0
        else:
            # Fin de la Phase 5
            st.session_state.game_over = True
            return

    st.session_state.current_gage = engine.get_next_gage(
        st.session_state.current_phase,
        st.session_state.next_player,
        st.session_state.history,
        st.session_state.accepted_tags
    )

def skip_turn():
    st.session_state.current_gage = engine.get_next_gage(
        st.session_state.current_phase,
        st.session_state.next_player,
        st.session_state.history,
        st.session_state.accepted_tags
    )

def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def calculate_distribution(total):
    # Ratio: 5, 4, 3, 2, 1 (total shares = 15)
    p1 = round(total * 5 / 15)
    p2 = round(total * 4 / 15)
    p3 = round(total * 3 / 15)
    p4 = round(total * 2 / 15)
    p5 = total - (p1 + p2 + p3 + p4)
    return {1: p1, 2: p2, 3: p3, 4: p4, 5: p5}

# --- SAFE WORD ---
st.markdown('<div class="safe-word">', unsafe_allow_html=True)
if st.button("STOP", key="stop_btn"):
    reset_game()
st.markdown('</div>', unsafe_allow_html=True)

def format_gage_text(text):
    import re
    h_name = st.session_state.names["Homme"]
    f_name = st.session_state.names["Femme"]
    
    # Remplacements pour la Femme
    text = re.sub(r"la [Ff]emme", f_name, text)
    # Remplacements pour l'Homme (gère l'apostrophe droite et courbe)
    text = re.sub(r"l['’][Hh]omme", h_name, text)
    return text

# --- SETUP SCREEN ---
if not st.session_state.get('game_started', False):
    st.title("🔥 Hot Escalation")
    st.markdown("### Préparez votre soirée...")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.names["Homme"] = st.text_input("Prénom Lui", value="Iz")
    with col2:
        st.session_state.names["Femme"] = st.text_input("Prénom Elle", value="Fa")
        
    st.markdown("---")
    
    all_tags = ['69', 'alcool', 'anal', 'anulingus', 'baiser', 'bandeau', 'body_shot', 'caresse', 'caresses', 'clito', 'compliment', 'cowgirl', 'cunnilingus', 'danse', 'denial', 'déshabillage', 'dirtytalk', 'doigts', 'edging', 'eye_contact', 'fantasy', 'fellation', 'fessée', 'grinding', 'hairpulling', 'hardcore', 'huile', 'ice', 'intense', 'jeu', 'jouet', 'lapdance', 'levrette', 'lubrifiant', 'massage', 'masturbation', 'menottes', 'missionnaire', 'oral', 'plug', 'plume', 'prep', 'pénétration', 'rétention', 'seins', 'sensuel', 'sexe', 'simulation', 'slow', 'softcore', 'striptease', 'teasing', 'temperature_play', 'titjob', 'vibration', 'visuel', 'whisper']
    
    st.markdown("#### Tags acceptés")
    st.session_state.accepted_tags = st.multiselect(
        "Cochez ce que vous acceptez ce soir :",
        options=all_tags,
        default=all_tags
    )
    
    col3, col4 = st.columns(2)
    with col3:
        num_gages = st.select_slider(
            "Nombre de gages",
            options=[15, 20, 25, 30, 35, 40, 45, 50, 55, 60],
            value=30
        )
        st.session_state.total_gages_target = num_gages
        st.session_state.phase_distribution = calculate_distribution(num_gages)
        
    with col4:
        st.session_state.sex_finality = st.toggle("Finalité Sexe", value=True)
        
    if st.button("COMMENCER L'ASCENSION"):
        if not st.session_state.accepted_tags:
            st.error("Veuillez choisir au moins quelques tags.")
        else:
            st.session_state.game_started = True
            st.session_state.start_time = time.time()
            st.session_state.total_done = 0
            st.session_state.gages_in_current_phase = 0
            st.session_state.current_phase = 1
            st.session_state.current_gage = engine.get_next_gage(
                st.session_state.current_phase,
                st.session_state.next_player,
                st.session_state.history,
                st.session_state.accepted_tags
            )
            st.rerun()

# --- GAME OVER SCREEN ---
elif st.session_state.get('game_over', False):
    st.title("❤️ Ascension Terminée")
    st.markdown("""
    <div class="gage-card">
        <div class="gage-text">
            L'ascension est terminée. Profitez de ce moment l'un avec l'autre...
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("RECOMMENCER"):
        reset_game()

# --- GAME SCREEN ---
else:
    # Header Info
    done = st.session_state.total_done
    total = st.session_state.total_gages_target
    remaining = max(total - done, 0)
    
    st.markdown(f'<div class="phase-info">Phase {st.session_state.current_phase} • {done} gages faits / {remaining} restants</div>', unsafe_allow_html=True)
    st.progress(done / total if total > 0 else 0)
    
    if st.session_state.current_gage:
        target_name = st.session_state.names[st.session_state.current_gage['target']]
        target_class = "player-homme" if st.session_state.current_gage['target'] == "Homme" else "player-femme"
        
        display_text = format_gage_text(st.session_state.current_gage['text'])
        
        # Gage Card
        st.markdown(f"""
        <div class="gage-card">
            <div class="player-name {target_class}">{target_name}</div>
            <div class="gage-text">{display_text}</div>
            <div class="tags-container">
                {" ".join([f'<span class="tag-badge">#{t}</span>' for t in st.session_state.current_gage['tags']])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Drink Suggestion
        if st.session_state.drink_counter >= 4:
            if random.random() > 0.5:
                st.markdown(f'<div class="drink-suggestion">🍹 {engine.get_drink_suggestion()}</div>', unsafe_allow_html=True)
                st.session_state.drink_counter = 0

        # Timer Section
        if st.session_state.current_gage.get('duration', 0) > 0:
            st.markdown("---")
            duration = st.session_state.current_gage['duration']
            
            col_t1, col_t2, col_t3 = st.columns([1, 2, 1])
            with col_t2:
                if not st.session_state.timer_active:
                    if st.button(f"⏱️ DÉMARRER LE MINUTEUR ({duration}s)"):
                        st.session_state.timer_active = True
                        st.session_state.timer_seconds = duration
                        st.rerun()
                else:
                    timer_placeholder = st.empty()
                    progress_bar = st.progress(1.0)
                    
                    # Logique du compte à rebours
                    for i in range(st.session_state.timer_seconds, -1, -1):
                        if not st.session_state.timer_active: break
                        
                        mins, secs = divmod(i, 60)
                        timer_placeholder.markdown(f"<h2 style='font-size: 3rem;'>{mins:02d}:{secs:02d}</h2>", unsafe_allow_html=True)
                        progress_bar.progress(i / duration)
                        time.sleep(1)
                    
                    if st.session_state.timer_active:
                        st.session_state.timer_active = False
                        st.success("Temps écoulé !")
                        st.balloons()
                        
                        import os
                        import base64
                        sound_file = "assets/sounds/success.mp3"
                        if os.path.exists(sound_file):
                            with open(sound_file, "rb") as f:
                                data = f.read()
                                b64 = base64.b64encode(data).decode()
                                audio_html = f"""
                                    <audio autoplay="true" style="display:none;">
                                        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                                    </audio>
                                """
                                st.markdown(audio_html, unsafe_allow_html=True)
                        
                        time.sleep(3)
                        st.rerun()

        # Buttons
        col_a, col_b = st.columns([3, 1])
        with col_a:
            if st.button("SUIVANT"):
                st.session_state.timer_active = False
                next_turn()
                st.rerun()
        with col_b:
            if st.button("PASSER"):
                st.session_state.timer_active = False
                skip_turn()
                st.rerun()
                
    else:
        st.markdown("""
        <div class="gage-card">
            <div class="gage-text">Plus de gages disponibles avec vos filtres dans cette phase.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("PASSER À LA PHASE SUIVANTE"):
            st.session_state.current_phase = min(st.session_state.current_phase + 1, 5)
            st.session_state.gages_in_current_phase = 0
            st.session_state.current_gage = engine.get_next_gage(
                st.session_state.current_phase,
                st.session_state.next_player,
                st.session_state.history,
                st.session_state.accepted_tags
            )
            st.rerun()

    # Manual Phase override (Discret)
    with st.expander("Contrôles avancés"):
        new_phase = st.number_input("Changer de phase manuellement", 1, 5, value=st.session_state.current_phase)
        if new_phase != st.session_state.current_phase:
            st.session_state.current_phase = new_phase
            st.session_state.gages_in_current_phase = 0
            st.session_state.current_gage = engine.get_next_gage(
                st.session_state.current_phase,
                st.session_state.next_player,
                st.session_state.history,
                st.session_state.accepted_tags
            )
            st.rerun()

```

# FILE: app_snapshot.md
```md

```

# FILE: requirements.txt
```txt
streamlit
pandas

```

# FILE: snapshot.py
```py
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
```

# FILE: assets\style.css
```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Raleway:wght@300;400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0E1117;
    font-family: 'Raleway', sans-serif;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif;
    color: #D4AF37;
    text-align: center;
}

.stButton>button {
    width: 100%;
    border-radius: 20px;
    height: 3em;
    background-color: #1a1c23;
    color: #D4AF37;
    border: 1px solid #D4AF37;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background-color: #D4AF37;
    color: #0E1117;
    box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
}

.gage-card {
    background: linear-gradient(145deg, #1a1c23, #0e1117);
    padding: 2.5rem;
    border-radius: 25px;
    border: 1px solid #3d3d3d;
    text-align: center;
    margin: 2rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.player-name {
    font-size: 2.5rem;
    font-family: 'Playfair Display', serif;
    margin-bottom: 1rem;
    font-style: italic;
}

.player-homme {
    color: #8A2BE2; /* Violet profond */
    text-shadow: 0 0 10px rgba(138, 43, 226, 0.3);
}

.player-femme {
    color: #FF1493; /* Rose profond */
    text-shadow: 0 0 10px rgba(255, 20, 147, 0.3);
}

.gage-text {
    font-size: 1.4rem;
    line-height: 1.6;
    color: #FAFAFA;
    margin-bottom: 2rem;
}

.tag-badge {
    display: inline-block;
    padding: 0.2rem 0.8rem;
    background-color: #262730;
    color: #888;
    border-radius: 10px;
    font-size: 0.8rem;
    margin: 0.2rem;
    border: 1px solid #333;
}

.safe-word {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
}

.safe-word button {
    background-color: #8B0000 !important;
    color: white !important;
    border: none !important;
    width: auto !important;
    padding: 0 20px !important;
}

.drink-suggestion {
    background-color: rgba(212, 175, 55, 0.1);
    border: 1px dashed #D4AF37;
    padding: 1rem;
    border-radius: 15px;
    color: #D4AF37;
    font-style: italic;
    margin-top: 1rem;
}

.phase-info {
    text-align: center;
    color: #888;
    font-size: 0.9rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* Custom progress bar */
.stProgress > div > div > div > div {
    background-color: #D4AF37;
}

```

# FILE: data\gages.json
```json
[
  // ==========================================
  // PHASE 1
  // ==========================================
  {
    "id": 1,
    "phase": 1,
    "target": "Homme",
    "text": "Embrasse langoureusement la Femme pendant 60 secondes en tenant son visage entre tes mains.",
    "tags": [
      "baiser",
      "sensuel",
      "slow",
      "softcore"
    ],
    "hot": 1,
    "duration": 60
  },
  {
    "id": 2,
    "phase": 1,
    "target": "Femme",
    "text": "Assieds-toi sur les genoux de l’Homme face à lui et fais-lui un massage des épaules et du cou pendant 90 secondes.",
    "tags": [
      "massage",
      "caresses",
      "softcore"
    ],
    "hot": 1,
    "duration": 90
  },
  {
    "id": 3,
    "phase": 1,
    "target": "Homme",
    "text": "Caresse les cuisses et les fesses de la Femme par-dessus ses vêtements pendant 60 secondes.",
    "tags": [
      "teasing",
      "caresses",
      "softcore"
    ],
    "hot": 1,
    "duration": 60
  },
  {
    "id": 4,
    "phase": 1,
    "target": "Femme",
    "text": "Réalise un striptease lent et enlève seulement un vêtement.",
    "tags": [
      "striptease",
      "déshabillage",
      "softcore"
    ],
    "hot": 1,
    "duration": 0
  },
  {
    "id": 5,
    "phase": 1,
    "target": "Femme",
    "text": "Caresse l'intérieur des cuisses de l’Homme pendant 1 minute",
    "tags": [
      "caresse",
      "softcore"
    ],
    "hot": 1,
    "duration": 60
  },
  {
    "id": 6,
    "phase": 1,
    "target": "Homme",
    "text": "Bois un verre entier de bière lentement.",
    "tags": [
      "alcool"
    ],
    "hot": 1,
    "duration": 0
  },
  {
    "id": 7,
    "phase": 1,
    "target": "Femme",
    "text": "Bois un shot de Gin.",
    "tags": [
      "alcool"
    ],
    "hot": 1,
    "duration": 0
  },
  {
    "id": 8,
    "phase": 1,
    "target": "Homme",
    "text": "Masse les pieds de la Femme pendant 1 minute.",
    "tags": [
      "massage",
      "softcore"
    ],
    "hot": 1,
    "duration": 60
  },
  {
    "id": 9,
    "phase": 1,
    "target": "Homme",
    "text": "Caresse le ventre et l'intérieur des cuisses de la Femme par-dessus ses vêtements pendant 60 secondes.",
    "tags": [
      "teasing",
      "caresses",
      "softcore"
    ],
    "hot": 1,
    "duration": 60
  },
  {
    "id": 10,
    "phase": 1,
    "target": "Femme",
    "text": "Embrasse l’Homme avec un french kiss profond pendant 45 secondes.",
    "tags": [
      "baiser",
      "softcore"
    ],
    "hot": 1,
    "duration": 45
  },
  {
    "id": 11,
    "phase": 1,
    "target": "Homme",
    "text": "Utilise le masse-tête sur la Femme pendant 1 minute.",
    "tags": [
      "massage",
      "softcore"
    ],
    "hot": 1,
    "duration": 60
  },
  {
    "id": 12,
    "phase": 1,
    "target": "Homme",
    "text": "Bande les yeux de la Femme et caresse son visage et son cou pendant 30 secondes.",
    "tags": [
      "bandeau",
      "sensuel",
      "softcore"
    ],
    "hot": 1,
    "duration": 30
  },
  {
    "id": 13,
    "phase": 1,
    "target": "Homme",
    "text": "Caresse les cheveux et le dos de la Femme pendant 1 minute.",
    "tags": [
      "caresses",
      "sensuel",
      "softcore"
    ],
    "hot": 1,
    "duration": 60
  },
  {
    "id": 14,
    "phase": 1,
    "target": "Homme",
    "text": "Bois une gorgée de gin ou de cocktail.",
    "tags": [
      "alcool"
    ],
    "hot": 1,
    "duration": 0
  },
  {
    "id": 15,
    "phase": 1,
    "target": "Femme",
    "text": "Lèche lentement les lèvres et le cou de l’Homme.",
    "tags": [
      "baiser",
      "softcore"
    ],
    "hot": 1,
    "duration": 0
  },
  {
    "id": 16,
    "phase": 1,
    "target": "Homme",
    "text": "Bande les yeux de la Femme et caresse ses bras et jambes avec la plume.",
    "tags": [
      "bandeau",
      "plume",
      "softcore"
    ],
    "hot": 1,
    "duration": 0
  },
  {
    "id": 17,
    "phase": 1,
    "target": "Femme",
    "text": "Fais un massage de la tête et des tempes de l’Homme pendant 90 secondes.",
    "tags": [
      "massage",
      "softcore"
    ],
    "hot": 1,
    "duration": 90
  },
  {
    "id": 18,
    "phase": 1,
    "target": "Homme",
    "text": "Bois la moitié d’une bière.",
    "tags": [
      "alcool"
    ],
    "hot": 1,
    "duration": 0
  },
  {
    "id": 19,
    "phase": 1,
    "target": "Homme",
    "text": "Simule des gémissements orgasmiques",
    "tags": [
      "baiser",
      "softcore"
    ],
    "hot": 1,
    "duration": 0
  },
  {
    "id": 20,
    "phase": 1,
    "target": "Homme",
    "text": "Masse les épaules de la Femme pendant 1 minute.",
    "tags": [
      "massage",
      "huile",
      "softcore"
    ],
    "hot": 1,
    "duration": 60
  },
  {
    "id": 21,
    "phase": 1,
    "target": "Homme",
    "text": "Regarde la Femme dans les yeux et dis-lui lentement 3 compliments très coquins sur son corps tout en lui caressant doucement le visage pendant 60 secondes.",
    "tags": [
      "dirtytalk",
      "compliment",
      "baiser",
      "sensuel",
      "softcore",
      "eye_contact"
    ],
    "hot": 1,
    "duration": 60
  },
  {
    "id": 22,
    "phase": 1,
    "target": "Homme",
    "text": "Place un glaçon entre tes lèvres et fais-le glisser lentement sur le cou, la poitrine et le ventre de la Femme pendant 60 secondes.",
    "tags": [
      "ice",
      "teasing",
      "sensuel",
      "softcore",
      "temperature_play"
    ],
    "hot": 1,
    "duration": 60
  },
  {
    "id": 23,
    "phase": 1,
    "target": "Femme",
    "text": "Assieds-toi dos contre l’Homme, ferme les yeux et guide ses mains pour qu’il te caresse les bras, les épaules et le cou pendant 90 secondes.",
    "tags": [
      "caresses",
      "guidage",
      "sensuel",
      "softcore"
    ],
    "hot": 1,
    "duration": 90
  },
  {
    "id": 24,
    "phase": 1,
    "target": "Homme",
    "text": "Fais un massage des mains et des avant-bras de la Femme avec de l’huile chaude pendant 2 minutes.",
    "tags": [
      "massage",
      "huile",
      "softcore",
      "sensuel"
    ],
    "hot": 1,
    "duration": 120
  },
  {
    "id": 25,
    "phase": 1,
    "target": "Homme",
    "text": "Bois un verre de bière lentement tout en regardant la Femme dans les yeux sans parler pendant toute la durée.",
    "tags": [
      "alcool",
      "eye_contact",
      "softcore"
    ],
    "hot": 2,
    "duration": 0
  },
  {
    "id": 26,
    "phase": 1,
    "target": "Homme",
    "text": "Masse les seins de la Femme par-dessus son soutien-gorge pendant 60 secondes.",
    "tags": [
      "seins",
      "caresses",
      "softcore"
    ],
    "hot": 2,
    "duration": 60
  },
  {
    "id": 27,
    "phase": 1,
    "target": "Femme",
    "text": "Embrasse et lèche le torse et les tétons de l’Homme pendant 30 secondes.",
    "tags": [
      "oral",
      "teasing",
      "softcore"
    ],
    "hot": 2,
    "duration": 30
  },
  {
    "id": 28,
    "phase": 1,
    "target": "Homme",
    "text": "Bande les yeux de la Femme et caresse tout son corps avec la plume pendant 2 minutes.",
    "tags": [
      "plume",
      "bandeau",
      "teasing",
      "softcore"
    ],
    "hot": 2,
    "duration": 120
  },
  {
    "id": 29,
    "phase": 1,
    "target": "Femme",
    "text": "Fais un lapdance habillée sur l’Homme pendant 60 secondes.",
    "tags": [
      "lapdance",
      "grinding",
      "softcore"
    ],
    "hot": 2,
    "duration": 60
  },
  {
    "id": 30,
    "phase": 1,
    "target": "Homme",
    "text": "Embrasse le ventre de la Femme en descendant lentement pendant 60 secondes.",
    "tags": [
      "baiser",
      "teasing",
      "softcore"
    ],
    "hot": 2,
    "duration": 60
  },
  {
    "id": 31,
    "phase": 1,
    "target": "Femme",
    "text": "Caresse le sexe de l’Homme par-dessus son pantalon pendant 45 secondes.",
    "tags": [
      "teasing",
      "caresses",
      "softcore"
    ],
    "hot": 2,
    "duration": 45
  },
  {
    "id": 32,
    "phase": 1,
    "target": "Femme",
    "text": "Assieds-toi dos contre l’Homme et frotte-toi doucement contre lui pendant 60 secondes.",
    "tags": [
      "grinding",
      "teasing",
      "softcore"
    ],
    "hot": 2,
    "duration": 60
  },
  {
    "id": 33,
    "phase": 1,
    "target": "Femme",
    "text": "Embrasse le torse de l’Homme tout en caressant ses bras pendant 30 secondes.",
    "tags": [
      "baiser",
      "caresses",
      "softcore"
    ],
    "hot": 2,
    "duration": 30
  },
  {
    "id": 34,
    "phase": 1,
    "target": "Femme",
    "text": "Danse sensuellement contre le corps de l’Homme pendant 90 secondes.",
    "tags": [
      "striptease",
      "teasing",
      "softcore"
    ],
    "hot": 2,
    "duration": 90
  },
  {
    "id": 35,
    "phase": 1,
    "target": "Homme",
    "text": "Caresse les seins de la Femme par-dessus ses vêtements pendant 60 secondes.",
    "tags": [
      "seins",
      "caresses",
      "softcore"
    ],
    "hot": 2,
    "duration": 60
  },
  {
    "id": 36,
    "phase": 1,
    "target": "Homme",
    "text": "Masse les fesses de la Femme pendant 1 minute.",
    "tags": [
      "massage",
      "teasing",
      "softcore"
    ],
    "hot": 2,
    "duration": 60
  },
  {
    "id": 37,
    "phase": 1,
    "target": "Femme",
    "text": "Frotte ta poitrine contre le torse de l’Homme pendant 90 secondes.",
    "tags": [
      "grinding",
      "teasing",
      "softcore"
    ],
    "hot": 2,
    "duration": 90
  },
  {
    "id": 38,
    "phase": 1,
    "target": "Homme",
    "text": "Caresse les fesses de la Femme par-dessus ses vêtements pendant 60 secondes.",
    "tags": [
      "teasing",
      "caresses",
      "softcore"
    ],
    "hot": 2,
    "duration": 60
  },
  {
    "id": 39,
    "phase": 1,
    "target": "Femme",
    "text": "Embrasse et mordille doucement les oreilles de l’Homme.",
    "tags": [
      "baiser",
      "softcore"
    ],
    "hot": 2,
    "duration": 0
  },
  {
    "id": 40,
    "phase": 1,
    "target": "Femme",
    "text": "Caresse le torse de l’Homme avec tes ongles doucement pendant 75 secondes.",
    "tags": [
      "caresses",
      "teasing",
      "softcore"
    ],
    "hot": 2,
    "duration": 75
  },
  {
    "id": 41,
    "phase": 1,
    "target": "Femme",
    "text": "Assieds-toi sur les genoux de l’Homme et frotte-toi légèrement contre lui.",
    "tags": [
      "grinding",
      "softcore"
    ],
    "hot": 2,
    "duration": 0
  },
  {
    "id": 42,
    "phase": 1,
    "target": "Femme",
    "text": "Réalise un strip-tease lent d’un seul accessoire (2 minutes).",
    "tags": [
      "striptease",
      "softcore"
    ],
    "hot": 2,
    "duration": 120
  },
  {
    "id": 43,
    "phase": 1,
    "target": "Homme",
    "text": "Caresse le dos de la Femme sous ses vêtements.",
    "tags": [
      "caresses",
      "softcore"
    ],
    "hot": 2,
    "duration": 0
  },
  {
    "id": 44,
    "phase": 1,
    "target": "Femme",
    "text": "Embrasse l’Homme avec un french kiss tout en caressant sa nuque.",
    "tags": [
      "baiser",
      "softcore"
    ],
    "hot": 2,
    "duration": 0
  },
  {
    "id": 45,
    "phase": 1,
    "target": "Homme",
    "text": "Chuchote à l’oreille de la Femme un fantasme doux et excitant que tu as sur elle pendant 30 secondes tout en lui caressant la nuque.",
    "tags": [
      "dirtytalk",
      "whisper",
      "fantasy",
      "sensuel",
      "softcore"
    ],
    "hot": 2,
    "duration": 60
  },
  {
    "id": 46,
    "phase": 1,
    "target": "Femme",
    "text": "Bois une gorgée de cocktail, garde-la en bouche et embrasse langoureusement l’Homme pour la partager avec lui.",
    "tags": [
      "alcool",
      "baiser",
      "sensuel",
      "softcore"
    ],
    "hot": 2,
    "duration": 45
  },
  {
    "id": 47,
    "phase": 1,
    "target": "Homme",
    "text": "Décris à voix haute ce que tu as envie de faire à la Femme dans les 30 prochaines minutes, avec des détails sensuels et excitants.",
    "tags": [
      "dirtytalk",
      "fantasy",
      "teasing",
      "softcore"
    ],
    "hot": 2,
    "duration": 60
  },
  {
    "id": 48,
    "phase": 1,
    "target": "Homme",
    "text": "Bois une gorgée de bière, garde-la en bouche quelques secondes puis embrasse langoureusement la Femme pour partager la fraîcheur.",
    "tags": [
      "alcool",
      "baiser",
      "sensuel",
      "softcore",
      "temperature_play"
    ],
    "hot": 2,
    "duration": 45
  },
  {
    "id": 49,
    "phase": 1,
    "target": "Femme",
    "text": "Utilise la plume pour dessiner lentement des formes sur tout le corps de l’Homme (torse, bras, cuisses) pendant 90 secondes.",
    "tags": [
      "plume",
      "teasing",
      "sensuel",
      "softcore"
    ],
    "hot": 2,
    "duration": 90
  },
  {
    "id": 50,
    "phase": 1,
    "target": "Femme",
    "text": "Bois un shot de gin puis garde la fraîcheur en bouche pendant 20 secondes avant d’embrasser l’Homme.",
    "tags": [
      "alcool",
      "baiser",
      "temperature_play",
      "softcore"
    ],
    "hot": 2,
    "duration": 30
  },
  {
    "id": 51,
    "phase": 1,
    "target": "Homme",
    "text": "Fais un body shot sur la Femme : verse un peu de cocktail sur son ventre et bois-le.",
    "tags": [
      "alcool",
      "body_shot",
      "oral",
      "teasing",
      "softcore"
    ],
    "hot": 3,
    "duration": 30
  },
  {
    "id": 52,
    "phase": 1,
    "target": "Femme",
    "text": "Masse les fesse de l’Homme très fort pendant 1 minute.",
    "tags": [
      "massage",
      "softcore"
    ],
    "hot": 3,
    "duration": 60
  },
  // ==========================================
  // PHASE 2
  // ==========================================
  {
    "id": 53,
    "phase": 2,
    "target": "Femme",
    "text": "Prépare un cocktail et fais-le boire à l’Homme directement à la paille tout en étant assise sur ses genoux.",
    "tags": [
      "alcool",
      "sensuel",
      "softcore"
    ],
    "hot": 1,
    "duration": 0
  },
  {
    "id": 54,
    "phase": 2,
    "target": "Homme",
    "text": "Bois un demi verre de cocktail en restant debout sur un pied.",
    "tags": "alcool",
    "hot": 1,
    "duration": 0
  },
  {
    "id": 55,
    "phase": 2,
    "target": "Femme",
    "text": "Bois un demi-verre de cocktail.",
    "tags": [
      "alcool"
    ],
    "hot": 2,
    "duration": 0
  },
  {
    "id": 56,
    "phase": 2,
    "target": "Homme",
    "text": "Bois deux verres de bière en moins de 90 secondes.",
    "tags": "alcool",
    "hot": 2,
    "duration": 90
  },
  {
    "id": 57,
    "phase": 2,
    "target": "Femme",
    "text": "Bois deux shots de gin l’un après l’autre.",
    "tags": "alcool",
    "hot": 2,
    "duration": 0
  },
  {
    "id": 58,
    "phase": 2,
    "target": "Femme",
    "text": "Fais un body shot : verse un peu de bière ou cocktail sur le torse de l’Homme et lèche-le lentement pendant 45 secondes.",
    "tags": [
      "alcool",
      "body_shot",
      "oral",
      "teasing",
      "softcore"
    ],
    "hot": 2,
    "duration": 45
  },
  {
    "id": 59,
    "phase": 2,
    "target": "Homme",
    "text": "Bois 3 gorgées de gin ou de cocktail en alternant avec des baisers légers sur le cou de la Femme.",
    "tags": [
      "alcool",
      "baiser",
      "softcore"
    ],
    "hot": 2,
    "duration": 45
  },
  {
    "id": 60,
    "phase": 2,
    "target": "Femme",
    "text": "Bois un demi-verre de bière en dansant sensuellement devant l’Homme.",
    "tags": [
      "alcool",
      "striptease",
      "softcore"
    ],
    "hot": 2,
    "duration": 60
  },
  {
    "id": 61,
    "phase": 2,
    "target": "Homme",
    "text": "Enlève le haut de la Femme et masse ses seins nus pendant 30 secondes.",
    "tags": [
      "seins",
      "caresses",
      "déshabillage",
      "softcore"
    ],
    "hot": 2,
    "duration": 30
  },
  {
    "id": 62,
    "phase": 2,
    "target": "Femme",
    "text": "Réalise un strip-tease complet jusqu’à rester en lingerie.",
    "tags": [
      "striptease",
      "déshabillage",
      "softcore"
    ],
    "hot": 2,
    "duration": 0
  },
  {
    "id": 63,
    "phase": 2,
    "target": "Femme",
    "text": "Fais un massage érotique du dos et des fesses de l’Homme.",
    "tags": [
      "massage",
      "huile",
      "softcore"
    ],
    "hot": 2,
    "duration": 0
  },
  {
    "id": 64,
    "phase": 2,
    "target": "Homme",
    "text": "Bois les deux tiers d’une bière.",
    "tags": [
      "alcool"
    ],
    "hot": 2,
    "duration": 0
  },
  {
    "id": 65,
    "phase": 2,
    "target": "Homme",
    "text": "Caresse tout le corps nu de la Femme avec la plume pendant 2 minutes.",
    "tags": [
      "plume",
      "teasing",
      "softcore"
    ],
    "hot": 2,
    "duration": 120
  },
  {
    "id": 66,
    "phase": 2,
    "target": "Homme",
    "text": "Enlève la culotte de la Femme avec tes dents.",
    "tags": [
      "striptease",
      "teasing",
      "déshabillage",
      "softcore"
    ],
    "hot": 2,
    "duration": 0
  },
  {
    "id": 67,
    "phase": 2,
    "target": "Femme",
    "text": "Bois un demi cocktail.",
    "tags": [
      "alcool"
    ],
    "hot": 2,
    "duration": 0
  },
  {
    "id": 68,
    "phase": 2,
    "target": "Homme",
    "text": "Caresse tout le corps nu de la Femme pendant 2 minutes.",
    "tags": [
      "caresses",
      "sensuel",
      "softcore"
    ],
    "hot": 2,
    "duration": 120
  },
  {
    "id": 69,
    "phase": 2,
    "target": "Homme",
    "text": "Bois un shot de gin ou de cocktail.",
    "tags": [
      "alcool"
    ],
    "hot": 2,
    "duration": 0
  },
  {
    "id": 70,
    "phase": 2,
    "target": "Homme",
    "text": "Lèche le ventre et les hanches de la Femme.",
    "tags": [
      "oral",
      "teasing",
      "softcore"
    ],
    "hot": 2,
    "duration": 0
  },
  {
    "id": 71,
    "phase": 2,
    "target": "Homme",
    "text": "La Femme choisit ta tenue et la danse à faire pendant 1 minute.",
    "tags": [
      "danse",
      "teasing"
    ],
    "hot": 2,
    "duration": 60
  },
  {
    "id": 72,
    "phase": 2,
    "target": "Femme",
    "text": "Lèche du whisky sur le corps de l’Homme.",
    "tags": [
      "oral",
      "alcool",
      "body_shot",
      "softcore"
    ],
    "hot": 2,
    "duration": 0
  },
  {
    "id": 73,
    "phase": 2,
    "target": "Homme",
    "text": "Bois les deux tiers d’un verre de bière tout en massant les épaules de la Femme en même temps.",
    "tags": [
      "alcool",
      "massage",
      "softcore"
    ],
    "hot": 2,
    "duration": 0
  },
  {
    "id": 74,
    "phase": 2,
    "target": "Femme",
    "text": "Prépare deux shots et fais un « shot à deux » : vous buvez en même temps tout en vous regardant dans les yeux.",
    "tags": [
      "alcool",
      "eye_contact",
      "softcore"
    ],
    "hot": 2,
    "duration": 0
  },
  {
    "id": 75,
    "phase": 2,
    "target": "Femme",
    "text": "Bois un verre de bière en chantant une chanson de ton choix.",
    "tags": "alcool",
    "hot": 2,
    "duration": 0
  },
  {
    "id": 76,
    "phase": 2,
    "target": "Homme",
    "text": "Prépare un cocktail et bois-le entièrement en moins de 90 secondes.",
    "tags": [
      "alcool"
    ],
    "hot": 2,
    "duration": 90
  },
  {
    "id": 77,
    "phase": 2,
    "target": "Femme",
    "text": "Fais une fellation lente et nue à l’Homme pendant 1 minute.",
    "tags": [
      "oral",
      "fellation",
      "softcore"
    ],
    "hot": 3,
    "duration": 60
  },
  {
    "id": 78,
    "phase": 2,
    "target": "Homme",
    "text": "Caresse le clitoris de la Femme avec tes doigts par-dessus sa culotte pendant 1 minutes.",
    "tags": [
      "doigts",
      "clito",
      "teasing",
      "masturbation",
      "softcore"
    ],
    "hot": 3,
    "duration": 60
  },
  {
    "id": 79,
    "phase": 2,
    "target": "Homme",
    "text": "Lèche les tétons de la Femme pendant 60 secondes.",
    "tags": [
      "oral",
      "seins",
      "softcore"
    ],
    "hot": 3,
    "duration": 60
  },
  {
    "id": 80,
    "phase": 2,
    "target": "Homme",
    "text": "Fais passer ton slip entre tes fesses et fais un strip-tease de 90 secondes.",
    "tags": [
      "striptease",
      "softcore"
    ],
    "hot": 3,
    "duration": 90
  },
  {
    "id": 81,
    "phase": 2,
    "target": "Femme",
    "text": "Lèche le périnée de l’Homme pendant 1 minute.",
    "tags": [
      "oral",
      "softcore"
    ],
    "hot": 3,
    "duration": 60
  },
  {
    "id": 82,
    "phase": 2,
    "target": "Femme",
    "text": "Chevauche l’Homme en culotte ou lingerie avec seulement un frottement extérieur pendant 1 minute.",
    "tags": [
      "grinding",
      "teasing",
      "softcore"
    ],
    "hot": 3,
    "duration": 60
  },
  {
    "id": 83,
    "phase": 2,
    "target": "Femme",
    "text": "Faites un 69 léger avec seulement des baisers et caresses pendant 1 minutes.",
    "tags": [
      "69",
      "oral",
      "softcore"
    ],
    "hot": 3,
    "duration": 60
  },
  {
    "id": 84,
    "phase": 2,
    "target": "Homme",
    "text": "Stimule le clitoris de la Femme avec tes doigts pendant 1 minute.",
    "tags": [
      "doigts",
      "clito",
      "masturbation",
      "softcore"
    ],
    "hot": 3,
    "duration": 60
  },
  {
    "id": 85,
    "phase": 2,
    "target": "Femme",
    "text": "Lèche les tétons de l’Homme tout en le branlant doucement.",
    "tags": [
      "oral",
      "doigts",
      "masturbation",
      "softcore"
    ],
    "hot": 3,
    "duration": 0
  },
  {
    "id": 86,
    "phase": 2,
    "target": "Homme",
    "text": "Fais un strip-tease torse nu pendant 2 minutes.",
    "tags": [
      "teasing",
      "striptease"
    ],
    "hot": 3,
    "duration": 120
  },
  {
    "id": 87,
    "phase": 2,
    "target": "Femme",
    "text": "Fais un titjob avec tes seins sur le sexe de l’Homme pendant 1 minute.",
    "tags": [
      "titjob",
      "teasing",
      "softcore"
    ],
    "hot": 3,
    "duration": 60
  },
  {
    "id": 88,
    "phase": 2,
    "target": "Homme",
    "text": "Déshabille-toi et prends une position souhaitée par la Femme. Elle peut prendre une photo.",
    "tags": [
      "bandeau",
      "plume",
      "doigts",
      "softcore"
    ],
    "hot": 3,
    "duration": 0
  },
  {
    "id": 89,
    "phase": 2,
    "target": "Femme",
    "text": "Fais un lapdance en lingerie sur l’Homme pendant 1 minute.",
    "tags": [
      "lapdance",
      "grinding",
      "softcore"
    ],
    "hot": 3,
    "duration": 60
  },
  {
    "id": 90,
    "phase": 2,
    "target": "Femme",
    "text": "Simule des gémissements jusqu'à l'orgasme.",
    "tags": [
      "simulation",
      "softcore"
    ],
    "hot": 3,
    "duration": 0
  },
  {
    "id": 91,
    "phase": 2,
    "target": "Homme",
    "text": "Stimule les seins et les tétons de la Femme pendant 1 minute.",
    "tags": [
      "seins",
      "caresses",
      "softcore"
    ],
    "hot": 3,
    "duration": 60
  },
  {
    "id": 92,
    "phase": 2,
    "target": "Femme",
    "text": "Bois un shot de gin ou de cocktail.",
    "tags": [
      "alcool"
    ],
    "hot": 3,
    "duration": 0
  },
  {
    "id": 93,
    "phase": 2,
    "target": "Femme",
    "text": "Frotte ton clitoris contre la cuisse de l’Homme.",
    "tags": [
      "grinding",
      "masturbation",
      "teasing",
      "softcore"
    ],
    "hot": 3,
    "duration": 0
  },
  {
    "id": 94,
    "phase": 2,
    "target": "Femme",
    "text": "Bois une rasade de bière.",
    "tags": [
      "alcool"
    ],
    "hot": 3,
    "duration": 0
  },
  {
    "id": 95,
    "phase": 2,
    "target": "Homme",
    "text": "Bande les yeux de la Femme et caresse l’intérieur de ses cuisses.",
    "tags": [
      "bandeau",
      "teasing",
      "softcore"
    ],
    "hot": 3,
    "duration": 0
  },
  {
    "id": 96,
    "phase": 2,
    "target": "Femme",
    "text": "Chevauche l’Homme en lingerie pendant 2 minutes.",
    "tags": [
      "grinding",
      "softcore"
    ],
    "hot": 3,
    "duration": 120
  },
  {
    "id": 97,
    "phase": 2,
    "target": "Homme",
    "text": "Caresse les fesses nues de la Femme.",
    "tags": [
      "caresses",
      "softcore"
    ],
    "hot": 3,
    "duration": 0
  },
  {
    "id": 98,
    "phase": 2,
    "target": "Femme",
    "text": "Lèche le périnée et les testicules de l’Homme.",
    "tags": [
      "oral",
      "softcore"
    ],
    "hot": 3,
    "duration": 0
  },
  {
    "id": 99,
    "phase": 2,
    "target": "Homme",
    "text": "Tease l’anus de la Femme pendant 1 minute. Elle choisit la langue ou le doigt.",
    "tags": [
      "anal",
      "prep",
      "doigts",
      "softcore"
    ],
    "hot": 3,
    "duration": 60
  },
  {
    "id": 100,
    "phase": 2,
    "target": "Femme",
    "text": "Tease l’anus de l’Homme lentement pendant 1 minute. Elle choisit la langue ou le doigt.",
    "tags": [
      "anal",
      "prep",
      "doigts",
      "softcore"
    ],
    "hot": 3,
    "duration": 60
  },
  {
    "id": 101,
    "phase": 2,
    "target": "Femme",
    "text": "Embrasse l’Homme profondément tout en caressant son sexe.",
    "tags": [
      "baiser",
      "teasing",
      "softcore"
    ],
    "hot": 3,
    "duration": 0
  },
  {
    "id": 102,
    "phase": 2,
    "target": "Homme",
    "text": "Stimule le clitoris de la Femme avec la plume.",
    "tags": [
      "plume",
      "clito",
      "masturbation",
      "softcore"
    ],
    "hot": 3,
    "duration": 0
  },
  {
    "id": 103,
    "phase": 2,
    "target": "Femme",
    "text": "Retiens ton excitation pendant 1 minute (edging) pendant qu'on te lèche les seins.",
    "tags": [
      "edging",
      "rétention",
      "softcore"
    ],
    "hot": 3,
    "duration": 60
  },
  {
    "id": 104,
    "phase": 2,
    "target": "Homme",
    "text": "Caresse doucement l'extérieur des lèvres de la Femme.",
    "tags": [
      "anal",
      "prep",
      "softcore"
    ],
    "hot": 3,
    "duration": 0
  },
  {
    "id": 105,
    "phase": 2,
    "target": "Femme",
    "text": "Fais un lapdance accompagné de baisers profonds.",
    "tags": [
      "lapdance",
      "baiser",
      "softcore"
    ],
    "hot": 3,
    "duration": 0
  },
  {
    "id": 106,
    "phase": 2,
    "target": "Femme",
    "text": "Assieds-toi habillée sur les genoux de l’Homme face à lui, regarde-le dans les yeux et dis-lui des mots cochons pendant que tu te frottes doucement contre lui pendant 60 secondes.",
    "tags": [
      "grinding",
      "dirtytalk",
      "eye_contact",
      "teasing",
      "softcore"
    ],
    "hot": 3,
    "duration": 60
  },
  {
    "id": 107,
    "phase": 2,
    "target": "Homme",
    "text": "Verse un peu de bière froide sur les seins de la Femme et lèche-la lentement tout en lui murmurant à quel point elle est excitante.",
    "tags": [
      "alcool",
      "body_shot",
      "oral",
      "dirtytalk",
      "softcore"
    ],
    "hot": 3,
    "duration": 60
  },
  {
    "id": 108,
    "phase": 2,
    "target": "Femme",
    "text": "Fais un strip-tease très lent tout en décrivant à voix haute ce que tu veux que l’Homme te fasse ensuite.",
    "tags": [
      "striptease",
      "dirtytalk",
      "teasing",
      "softcore"
    ],
    "hot": 3,
    "duration": 90
  },
  {
    "id": 109,
    "phase": 2,
    "target": "Homme",
    "text": "Bois un shot puis fais un massage sensuel des seins et du ventre de la Femme avec de l’huile tout en lui disant des mots très chauds.",
    "tags": [
      "alcool",
      "massage",
      "seins",
      "dirtytalk",
      "huile",
      "softcore"
    ],
    "hot": 3,
    "duration": 90
  },
  {
    "id": 110,
    "phase": 2,
    "target": "Femme",
    "text": "Allonge-toi nue sur le ventre. L’Homme verse de l’huile tiède sur ton dos et masse lentement en descendant vers les fesses pendant 3 minutes.",
    "tags": [
      "massage",
      "huile",
      "teasing",
      "softcore"
    ],
    "hot": 3,
    "duration": 180
  },
  {
    "id": 111,
    "phase": 2,
    "target": "Homme",
    "text": "Bois un shot de gin, puis utilise ta langue froide pour tracer un chemin depuis le nombril de la Femme jusqu’à l’intérieur de ses cuisses.",
    "tags": [
      "alcool",
      "oral",
      "teasing",
      "temperature_play",
      "softcore"
    ],
    "hot": 3,
    "duration": 60
  },
  {
    "id": 112,
    "phase": 2,
    "target": "Femme",
    "text": "Enfile les boules de geisha et fais une danse sensuelle ou marche lentement autour de la pièce pendant 90 secondes.",
    "tags": [
      "jouet",
      "teasing",
      "sensuel",
      "softcore"
    ],
    "hot": 3,
    "duration": 90
  },
  {
    "id": 113,
    "phase": 2,
    "target": "Homme",
    "text": "Bande les yeux de la Femme et fais-lui deviner quelle partie de ton corps tu poses contre sa peau (torse, mains, lèvres…) pendant 2 minutes.",
    "tags": [
      "bandeau",
      "jeu",
      "teasing",
      "sensuel",
      "softcore"
    ],
    "hot": 3,
    "duration": 120
  },
  {
    "id": 114,
    "phase": 2,
    "target": "Homme",
    "text": "Bois un grand verre de cocktail pendant que la Femme te fait un lapdance habillée.",
    "tags": [
      "alcool",
      "lapdance",
      "teasing",
      "softcore"
    ],
    "hot": 3,
    "duration": 60
  },
  {
    "id": 115,
    "phase": 2,
    "target": "Femme",
    "text": "Bois un verre de bière lentement tout en étant assise nue (ou en lingerie) sur les genoux de l’Homme en frottant doucement.",
    "tags": [
      "alcool",
      "grinding",
      "teasing",
      "softcore"
    ],
    "hot": 3,
    "duration": 0
  },
  // ==========================================
  // PHASE 3
  // ==========================================
  {
    "id": 116,
    "phase": 3,
    "target": "Femme",
    "text": "Déshabille-toi et prends ta position la plus obscène. L’Homme peut filmer.",
    "tags": [
      "softcore",
      "visuel"
    ],
    "hot": 2,
    "duration": 240
  },
  {
    "id": 117,
    "phase": 3,
    "target": "Homme",
    "text": "Bois un shot de gin ou de whisky.",
    "tags": [
      "alcool"
    ],
    "hot": 2,
    "duration": 0
  },
  {
    "id": 118,
    "phase": 3,
    "target": "Femme",
    "text": "Bois un shot de gin au citron.",
    "tags": [
      "alcool"
    ],
    "hot": 2,
    "duration": 0
  },
  {
    "id": 119,
    "phase": 3,
    "target": "Femme",
    "text": "Croise des cuisses et fais pression sur ton clitoris pendant que l’Homme te caresse les fesses 2 minutes",
    "tags": [
      "masturbation",
      "caresse",
      "softcore"
    ],
    "hot": 3,
    "duration": 120
  },
  {
    "id": 120,
    "phase": 3,
    "target": "Homme",
    "text": "Bois un shot de cocktail.",
    "tags": [
      "alcool"
    ],
    "hot": 3,
    "duration": 0
  },
  {
    "id": 121,
    "phase": 3,
    "target": "Femme",
    "text": "Bois une moitié de cocktail.",
    "tags": [
      "alcool"
    ],
    "hot": 3,
    "duration": 0
  },
  {
    "id": 122,
    "phase": 3,
    "target": "Femme",
    "text": "Lèche le torse de l’Homme en gémissant.",
    "tags": [
      "oral",
      "slow",
      "softcore"
    ],
    "hot": 3,
    "duration": 0
  },
  {
    "id": 123,
    "phase": 3,
    "target": "Homme",
    "text": "Fais un cunnilingus à la Femme pendant 2 minutes.",
    "tags": [
      "oral",
      "cunnilingus",
      "softcore"
    ],
    "hot": 4,
    "duration": 120
  },
  {
    "id": 124,
    "phase": 3,
    "target": "Femme",
    "text": "Masturbe-toi devant l’Homme pendant 2 minutes.",
    "tags": [
      "masturbation",
      "softcore"
    ],
    "hot": 4,
    "duration": 120
  },
  {
    "id": 125,
    "phase": 3,
    "target": "Homme",
    "text": "Utilise le rabbit vibrator sur le clitoris de la Femme pendant 2 minutes.",
    "tags": [
      "jouet",
      "vibration",
      "clito",
      "masturbation",
      "softcore"
    ],
    "hot": 4,
    "duration": 120
  },
  {
    "id": 126,
    "phase": 3,
    "target": "Femme",
    "text": "Fais une danse du choix de l’Homme tout en portant les boules de geisha.",
    "tags": [
      "oral",
      "jouet",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 127,
    "phase": 3,
    "target": "Homme",
    "text": "Combine doigts et cunnilingus pendant 2 minutes.",
    "tags": [
      "doigts",
      "oral",
      "softcore"
    ],
    "hot": 4,
    "duration": 120
  },
  {
    "id": 128,
    "phase": 3,
    "target": "Homme",
    "text": "Insère toi le plug anal et garde le pendant 3 tours.",
    "tags": [
      "anal",
      "plug",
      "lubrifiant",
      "prep",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 129,
    "phase": 3,
    "target": "Femme",
    "text": "Faites un 69 complet pendant 5 minutes.",
    "tags": [
      "69",
      "oral",
      "softcore"
    ],
    "hot": 4,
    "duration": 300
  },
  {
    "id": 130,
    "phase": 3,
    "target": "Homme",
    "text": "Utilise le rabbit tout en léchant les seins de la Femme.",
    "tags": [
      "jouet",
      "oral",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 131,
    "phase": 3,
    "target": "Femme",
    "text": "Danse avec les boules de geisha en toi.",
    "tags": [
      "jouet",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 132,
    "phase": 3,
    "target": "Homme",
    "text": "Insère doucement un doigt anal avec lubrifiant pendant 1 minute.",
    "tags": [
      "anal",
      "prep",
      "lubrifiant",
      "softcore"
    ],
    "hot": 4,
    "duration": 1
  },
  {
    "id": 133,
    "phase": 3,
    "target": "Homme",
    "text": "Place toi en levrette et reçoit une douce fessée.",
    "tags": [
      "levrette",
      "fessée"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 134,
    "phase": 3,
    "target": "Homme",
    "text": "Combine cunnilingus et rabbit.",
    "tags": [
      "oral",
      "jouet",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 135,
    "phase": 3,
    "target": "Femme",
    "text": "Place-toi en levrette et reçoit une fessée légère",
    "tags": [
      "fessée",
      "levrette"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 136,
    "phase": 3,
    "target": "Homme",
    "text": "Stimule le vagin et le clito avec tes doigts pendant 2 minutes.",
    "tags": [
      "doigts",
      "masturbation",
      "softcore"
    ],
    "hot": 4,
    "duration": 120
  },
  {
    "id": 137,
    "phase": 3,
    "target": "Femme",
    "text": "Chevauche le visage de l’Homme pendant 1 minute.",
    "tags": [
      "oral",
      "softcore"
    ],
    "hot": 4,
    "duration": 60
  },
  {
    "id": 138,
    "phase": 3,
    "target": "Homme",
    "text": "Fais de l'edging à la Femme pendant 3 minutes.",
    "tags": [
      "edging",
      "rétention",
      "masturbation",
      "softcore"
    ],
    "hot": 4,
    "duration": 180
  },
  {
    "id": 139,
    "phase": 3,
    "target": "Femme",
    "text": "Fais un hysterical literature.",
    "tags": [
      "jouet",
      "masturbation",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 140,
    "phase": 3,
    "target": "Homme",
    "text": "Fais-toi menoter nu et la Femme fais ce qu'elle veut.",
    "tags": [
      "menottes",
      "hardcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 141,
    "phase": 3,
    "target": "Homme",
    "text": "Fais un cunnilingus intense (lèche, aspire, accélère).",
    "tags": [
      "oral",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 142,
    "phase": 3,
    "target": "Femme",
    "text": "Alterne branlette rapide et lente (edging).",
    "tags": [
      "doigts",
      "masturbation",
      "edging",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 143,
    "phase": 3,
    "target": "Homme",
    "text": "Applique du lubrifiant et caresse analement.",
    "tags": [
      "anal",
      "lubrifiant",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 144,
    "phase": 3,
    "target": "Femme",
    "text": "Faites un 69 avec le rabbit.",
    "tags": [
      "69",
      "jouet",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 145,
    "phase": 3,
    "target": "Homme",
    "text": "Lèche le clitoris de la Femme en lui caressant un téton pendant 1 minute.",
    "tags": [
      "oral",
      "massage"
    ],
    "hot": 4,
    "duration": 60
  },
  {
    "id": 146,
    "phase": 3,
    "target": "Femme",
    "text": "Chevauche ton coussin pendant 2 minutes. Essaye de jouir",
    "tags": [
      "masturbation",
      "grinding"
    ],
    "hot": 4,
    "duration": 120
  },
  {
    "id": 147,
    "phase": 3,
    "target": "Homme",
    "text": "Utilise plusieurs jouets en même temps.",
    "tags": [
      "jouet",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 148,
    "phase": 3,
    "target": "Homme",
    "text": "Fais un French kiss d'une minute en doigtant un orifice de la femme",
    "tags": [
      "doigts",
      "anal",
      "baiser",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 149,
    "phase": 3,
    "target": "Homme",
    "text": "Mets-toi un plug anal et fait un strip-tease de 1 minute.",
    "tags": [
      "jouet",
      "striptease",
      "softcore"
    ],
    "hot": 4,
    "duration": 60
  },
  {
    "id": 150,
    "phase": 3,
    "target": "Femme",
    "text": "Mets-toi un plug anal et fait un strip-tease de 1 minute.",
    "tags": [
      "jouet",
      "striptease",
      "softcore"
    ],
    "hot": 4,
    "duration": 60
  },
  {
    "id": 151,
    "phase": 3,
    "target": "Homme",
    "text": "Simule une fellation",
    "tags": [
      "simulation",
      "fellation",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 152,
    "phase": 3,
    "target": "Femme",
    "text": "Fais une fellation tout en caressant tes seins.",
    "tags": [
      "oral",
      "seins",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 153,
    "phase": 3,
    "target": "Femme",
    "text": "Masturbe-toi (fingering) lentement devant l’Homme tout en lui décrivant tes sensations et ce que tu imagines qu’il te fasse.",
    "tags": [
      "masturbation",
      "dirtytalk",
      "teasing",
      "softcore",
      "eye_contact"
    ],
    "hot": 4,
    "duration": 120
  },
  {
    "id": 154,
    "phase": 3,
    "target": "Homme",
    "text": "Fais un cunnilingus pendant 3 minutes tout en alternant avec des phrases très sales et excitantes.",
    "tags": [
      "oral",
      "cunnilingus",
      "dirtytalk",
      "softcore"
    ],
    "hot": 4,
    "duration": 180
  },
  {
    "id": 155,
    "phase": 3,
    "target": "Femme",
    "text": "Utilise le rabbit sur toi tout en regardant l’Homme dans les yeux et en lui racontant un fantasme très détaillé.",
    "tags": [
      "jouet",
      "masturbation",
      "dirtytalk",
      "fantasy",
      "softcore"
    ],
    "hot": 4,
    "duration": 120
  },
  {
    "id": 156,
    "phase": 3,
    "target": "Femme",
    "text": "Allonge-toi et utilise le rabbit sur ton clitoris tout en respirant profondément et en comptant tes respirations à voix haute pendant 2 minutes.",
    "tags": [
      "jouet",
      "masturbation",
      "respiration",
      "softcore"
    ],
    "hot": 4,
    "duration": 120
  },
  {
    "id": 157,
    "phase": 3,
    "target": "Homme",
    "text": "Fais un cunnilingus très lent et doux pendant 2 minutes en variant la pression et en explorant différentes zones.",
    "tags": [
      "oral",
      "cunnilingus",
      "slow",
      "softcore"
    ],
    "hot": 4,
    "duration": 120
  },
  {
    "id": 158,
    "phase": 3,
    "target": "Femme",
    "text": "Utilise la plume et tes doigts pour caresser l’intérieur des cuisses, le ventre et autour du sexe de l’Homme sans le toucher directement pendant 2 minutes.",
    "tags": [
      "teasing",
      "plume",
      "denial",
      "softcore"
    ],
    "hot": 4,
    "duration": 120
  },
  {
    "id": 159,
    "phase": 3,
    "target": "Homme",
    "text": "Insère lentement le plug anal à la Femme avec beaucoup de lubrifiant tout en lui faisant un massage des fesses et du dos pendant 2 minutes.",
    "tags": [
      "anal",
      "plug",
      "lubrifiant",
      "prep",
      "massage",
      "softcore"
    ],
    "hot": 4,
    "duration": 120
  },
  {
    "id": 160,
    "phase": 3,
    "target": "Femme",
    "text": "Fais un deepthroat en regardant l’Homme dans les yeux.",
    "tags": [
      "oral",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 161,
    "phase": 3,
    "target": "Femme",
    "text": "Mets toi en levrette face au sol et gémis",
    "tags": [
      "levrette",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 162,
    "phase": 3,
    "target": "Femme",
    "text": "Fais-toi menotter et laisse l’Homme faire ce qu'il veut, sans pénétration.",
    "tags": [
      "menottes",
      "hardcore"
    ],
    "hot": 5,
    "duration": 0
  },
  // ==========================================
  // PHASE 4
  // ==========================================
  {
    "id": 163,
    "phase": 4,
    "target": "Homme",
    "text": "Pénètre vaginalement la Femme lentement pendant 2 minutes.",
    "tags": [
      "pénétration",
      "sexe",
      "slow",
      "softcore"
    ],
    "hot": 4,
    "duration": 120
  },
  {
    "id": 164,
    "phase": 4,
    "target": "Homme",
    "text": "Combine cunnilingus, doigts et plug anal.",
    "tags": [
      "oral",
      "anal",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 165,
    "phase": 4,
    "target": "Femme",
    "text": "Utilise le rabbit sur toi pendant que tu suces l’Homme.",
    "tags": [
      "jouet",
      "oral",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 166,
    "phase": 4,
    "target": "Femme",
    "text": "Bois un grand verre de cocktail.",
    "tags": [
      "alcool"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 167,
    "phase": 4,
    "target": "Homme",
    "text": "Faites un 69 très intense.",
    "tags": [
      "69",
      "oral",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 168,
    "phase": 4,
    "target": "Homme",
    "text": "Utilise tous les jouets en même temps sur la Femme.",
    "tags": [
      "jouet",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 169,
    "phase": 4,
    "target": "Femme",
    "text": "Pénètre-toi avec ton gode pendant 1 minutes. Vibration activée ou non.",
    "tags": [
      "masturbation",
      "jouet"
    ],
    "hot": 4,
    "duration": 240
  },
  {
    "id": 170,
    "phase": 4,
    "target": "Femme",
    "text": "Mets-toi un plug anal et les boules de geisha pendant 4 tours.",
    "tags": [
      "jouet"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 171,
    "phase": 4,
    "target": "Femme",
    "text": "Utilise les jouets sur l’Homme et arrange-toi pour que ce soit agréable.",
    "tags": [
      "jouet",
      "softcore"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 172,
    "phase": 4,
    "target": "Femme",
    "text": "Restez habillés, chevauche l’Homme en crachant des obscénités.",
    "tags": [
      "teasing",
      "dirtytalk",
      "cowgirl"
    ],
    "hot": 4,
    "duration": 0
  },
  {
    "id": 173,
    "phase": 4,
    "target": "Femme",
    "text": "Chevauche l’Homme en gardant le contrôle total pendant 2 minutes.",
    "tags": [
      "sexe",
      "cowgirl",
      "softcore"
    ],
    "hot": 5,
    "duration": 120
  },
  {
    "id": 174,
    "phase": 4,
    "target": "Homme",
    "text": "Combine pénétration vaginale et plug anal.",
    "tags": [
      "pénétration",
      "anal",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 175,
    "phase": 4,
    "target": "Femme",
    "text": "Lèche l'anus de l’Homme pendant 1 minute.",
    "tags": [
      "oral",
      "anulingus",
      "anal"
    ],
    "hot": 5,
    "duration": 60
  },
  {
    "id": 176,
    "phase": 4,
    "target": "Homme",
    "text": "Lèche l'anus de la Femme pendant 1 minute.",
    "tags": [
      "anulingus",
      "oral",
      "anal"
    ],
    "hot": 5,
    "duration": 60
  },
  {
    "id": 177,
    "phase": 4,
    "target": "Homme",
    "text": "Tente une pénétration anale avec les doigts ou la bite, très lente et préparée. Pas d'obligation de réussite.",
    "tags": [
      "anal",
      "doigts",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 178,
    "phase": 4,
    "target": "Homme",
    "text": "Baise la Femme fermement sans douleur.",
    "tags": [
      "sexe",
      "intense",
      "hardcore",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 179,
    "phase": 4,
    "target": "Femme",
    "text": "Chevauche l’Homme avec un plug anal en toi.",
    "tags": [
      "sexe",
      "anal",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 180,
    "phase": 4,
    "target": "Femme",
    "text": "Prends la position amazone pendant 2 minutes.",
    "tags": [
      "sexe",
      "softcore"
    ],
    "hot": 5,
    "duration": 120
  },
  {
    "id": 181,
    "phase": 4,
    "target": "Femme",
    "text": "Utilise ton vibro pendant 2 minutes que l’Homme te suce les seins.",
    "tags": [
      "oral",
      "jouet",
      "masturbation"
    ],
    "hot": 5,
    "duration": 120
  },
  {
    "id": 182,
    "phase": 4,
    "target": "Homme",
    "text": "Combine pénétration et stimulation anale.",
    "tags": [
      "pénétration",
      "anal",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 183,
    "phase": 4,
    "target": "Femme",
    "text": "Laisse l’Homme te prendre comme il veut pendant 2 minutes.",
    "tags": [
      "sexe",
      "intense",
      "hardcore",
      "softcore"
    ],
    "hot": 5,
    "duration": 120
  },
  {
    "id": 184,
    "phase": 4,
    "target": "Homme",
    "text": "Porte le plug anal pendant que tu pénètres la Femme.",
    "tags": [
      "anal",
      "sexe",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 185,
    "phase": 4,
    "target": "Homme",
    "text": "Prends la Femme en position cuillères profondes.",
    "tags": [
      "pénétration",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 186,
    "phase": 4,
    "target": "Femme",
    "text": "Contrôle ton propre orgasme (edging).",
    "tags": [
      "edging",
      "rétention",
      "masturbation",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 187,
    "phase": 4,
    "target": "Homme",
    "text": "Prends la Femme en levrette avec le gode.",
    "tags": [
      "pénétration",
      "jouet",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 188,
    "phase": 4,
    "target": "Femme",
    "text": "Déshabille-toi et frotte ton vagin sur le pénis de l’Homme en le chevauchant",
    "tags": [
      "sexe",
      "masturbation",
      "teasing",
      "cowgirl",
      "grinding"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 189,
    "phase": 4,
    "target": "Homme",
    "text": "Combine anal play et pénétration vaginale.",
    "tags": [
      "anal",
      "pénétration",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 190,
    "phase": 4,
    "target": "Homme",
    "text": "Trois coups en missionnaire avec les jambes de la Femme sur tes épaules.",
    "tags": [
      "pénétration",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 191,
    "phase": 4,
    "target": "Femme",
    "text": "Mets-toi des boules de geisha dans l'anus en gémissant.",
    "tags": [
      "anal",
      "masturbation",
      "hardcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 192,
    "phase": 4,
    "target": "Homme",
    "text": "Mets-toi des boules de geisha dans l'anus.",
    "tags": [
      "anal",
      "hardcore",
      "masturbation"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 193,
    "phase": 4,
    "target": "Homme",
    "text": "Réalise une pénétration anale complète très lente si acceptée.",
    "tags": [
      "anal",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 194,
    "phase": 4,
    "target": "Femme",
    "text": "Sexe oral mutuel très intense.",
    "tags": [
      "69",
      "oral",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 195,
    "phase": 4,
    "target": "Homme",
    "text": "Frotte le clitoris avec du lubrifiant sur les doigts en disant des mots cochons.",
    "tags": [
      "doigts",
      "lubrifiant",
      "hardcore",
      "dirtytalk",
      "clito"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 196,
    "phase": 4,
    "target": "Homme",
    "text": "Contrôle l’orgasme de la Femme.",
    "tags": [
      "edging",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 197,
    "phase": 4,
    "target": "Femme",
    "text": "Combine plusieurs jouets et oral.",
    "tags": [
      "jouet",
      "oral",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 198,
    "phase": 4,
    "target": "Homme",
    "text": "Frotte ton pénis sur les bords du vagin de la Femme sans pénétration.",
    "tags": [
      "teasing",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 199,
    "phase": 4,
    "target": "Femme",
    "text": "Prends le contrôle total pendant 7 minutes.",
    "tags": [
      "sexe",
      "softcore"
    ],
    "hot": 5,
    "duration": 420
  },
  {
    "id": 200,
    "phase": 4,
    "target": "Femme",
    "text": "Masturbe l’Homme avec tes seins et ta bouche.",
    "tags": [
      "titjob",
      "oral",
      "masturbation",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  // ==========================================
  // PHASE 5
  // ==========================================
  {
    "id": 201,
    "phase": 5,
    "target": "Homme",
    "text": "Baise la Femme dans ta position préférée pendant 2 minutes.",
    "tags": [
      "pénétration",
      "sexe",
      "hardcore",
      "softcore"
    ],
    "hot": 5,
    "duration": 120
  },
  {
    "id": 202,
    "phase": 5,
    "target": "Femme",
    "text": "Chevauche l’Homme brutalement pendant 30 secondes.",
    "tags": [
      "sexe",
      "cowgirl",
      "hardcore"
    ],
    "hot": 5,
    "duration": 30
  },
  {
    "id": 203,
    "phase": 5,
    "target": "Homme",
    "text": "Prends la Femme en levrette profonde pendant 1 minute.",
    "tags": [
      "pénétration",
      "levrette",
      "hardcore",
      "softcore"
    ],
    "hot": 5,
    "duration": 60
  },
  {
    "id": 204,
    "phase": 5,
    "target": "Homme",
    "text": "Pénètre la Femme tout en utilisant le plug anal sur elle.",
    "tags": [
      "pénétration",
      "anal",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 205,
    "phase": 5,
    "target": "Femme",
    "text": "Atteins plusieurs orgasmes avec le rabbit et l’Homme.",
    "tags": [
      "jouet",
      "masturbation",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 206,
    "phase": 5,
    "target": "Homme",
    "text": "Réalise une pénétration anale complète si accepté.",
    "tags": [
      "anal",
      "hardcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 207,
    "phase": 5,
    "target": "Femme",
    "text": "Bois un dernier verre puis baise l’Homme comme tu veux.",
    "tags": [
      "alcool",
      "sexe",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 208,
    "phase": 5,
    "target": "Homme",
    "text": "Prends la Femme en missionnaire avec les jambes relevées.",
    "tags": [
      "pénétration",
      "missionnaire",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 209,
    "phase": 5,
    "target": "Homme",
    "text": "Baise la Femme debout contre un mur.",
    "tags": [
      "sexe",
      "hardcore",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 210,
    "phase": 5,
    "target": "Femme",
    "text": "Chevauche l’Homme en amazone",
    "tags": [
      "sexe",
      "cowgirl",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 211,
    "phase": 5,
    "target": "Homme",
    "text": "Combine pénétration et stimulation du clito avec le rabbit.",
    "tags": [
      "pénétration",
      "jouet",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 212,
    "phase": 5,
    "target": "Femme",
    "text": "Laisse l’Homme te prendre en cuillères tout en te caressant les seins.",
    "tags": [
      "sexe",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 213,
    "phase": 5,
    "target": "Femme",
    "text": "Masturbe-toi devant l’Homme puis laisse-le te prendre.",
    "tags": [
      "masturbation",
      "teasing",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 214,
    "phase": 5,
    "target": "Homme",
    "text": "Prends la Femme en levrette avec hairpulling.",
    "tags": [
      "pénétration",
      "hairpulling",
      "hardcore",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 215,
    "phase": 5,
    "target": "Homme",
    "text": "Pénètre la Femme tout en utilisant le plug anal et le rabbit.",
    "tags": [
      "pénétration",
      "anal",
      "jouet",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 216,
    "phase": 5,
    "target": "Homme",
    "text": "Baise la Femme en missionnaire en la regardant dans les yeux.",
    "tags": [
      "pénétration",
      "missionnaire",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 217,
    "phase": 5,
    "target": "Femme",
    "text": "Retiens ton orgasme le plus longtemps possible puis lâche-toi.",
    "tags": [
      "edging",
      "rétention",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 218,
    "phase": 5,
    "target": "Homme",
    "text": "Prends la Femme par derrière avec beaucoup de lubrifiant.",
    "tags": [
      "pénétration",
      "lubrifiant",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 219,
    "phase": 5,
    "target": "Femme",
    "text": "Utilise tous les jouets sur toi pendant que l’Homme te regarde.",
    "tags": [
      "jouet",
      "masturbation",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 220,
    "phase": 5,
    "target": "Homme",
    "text": "Alterne pénétration vaginale et anal play.",
    "tags": [
      "pénétration",
      "anal",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 221,
    "phase": 5,
    "target": "Homme",
    "text": "Prends la Femme en position debout ou contre un meuble.",
    "tags": [
      "sexe",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 222,
    "phase": 5,
    "target": "Femme",
    "text": "Laisse l’Homme te doigter et te lécher jusqu’à l’orgasme.",
    "tags": [
      "doigts",
      "oral",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 223,
    "phase": 5,
    "target": "Homme",
    "text": "Pénètre lentement puis accélère progressivement.",
    "tags": [
      "pénétration",
      "teasing",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 224,
    "phase": 5,
    "target": "Homme",
    "text": "Pénètre en grands coups secs et puissant.",
    "tags": [
      "intense",
      "pénétration",
      "hardcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 225,
    "phase": 5,
    "target": "Homme",
    "text": "Baise la Femme en cuillères tout en stimulant son clito.",
    "tags": [
      "pénétration",
      "clito",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 226,
    "phase": 5,
    "target": "Homme",
    "text": "Prends la Femme comme tu veux pour le final.",
    "tags": [
      "sexe",
      "hardcore",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  },
  {
    "id": 227,
    "phase": 5,
    "target": "Femme",
    "text": "Laisse-toi prendre comme tu veux jusqu'à ce que l’Homme jouisse.",
    "tags": [
      "sexe",
      "softcore"
    ],
    "hot": 5,
    "duration": 0
  }
]
```

# FILE: scripts\generate_json.py
```py
import json
import re

gages_text = """
PHASE 1 – Échauffement & Connexion (Hot 1-2)
1.	Homme : Embrasse langoureusement la Femme pendant 60 secondes en tenant son visage entre tes mains. Tags: #baiser #sensuel #slow #softcore Hot: 1
2.	Femme : Assieds-toi sur les genoux de l’Homme face à lui et fais-lui un massage des épaules et du cou pendant 90 secondes. Tags: #massage #caresses #softcore Hot: 1
3.	Homme : Caresse les cuisses et les fesses de la Femme par-dessus ses vêtements pendant 75 secondes. Tags: #teasing #caresses #softcore Hot: 1
4.	Femme : Réalise un strip-tease lent et enlève seulement un vêtement. Tags: #striptease #déshabillage #softcore Hot: 1
5.	Homme : Masse les seins de la Femme par-dessus son soutien-gorge pendant 90 secondes. Tags: #seins #caresses #softcore Hot: 2
6.	Femme : Embrasse et lèche le torse et les tétons de l’Homme pendant 75 secondes. Tags: #oral #teasing #softcore Hot: 2
7.	Homme : Bande les yeux de la Femme et caresse tout son corps avec la plume pendant 2 minutes. Tags: #plume #bandeau #teasing #softcore Hot: 2
8.	Femme : Fais une fellation douce à l’Homme par-dessus son caleçon pendant 90 secondes. Tags: #oral #fellation #softcore Hot: 2
9.	Homme : Bois une bière entière lentement. Tags: #alcool Hot: 1
10.	Femme : Lèche le cou et les oreilles de l’Homme pendant 60 secondes. Tags: #baiser #teasing #softcore Hot: 1
11.	Homme : Massage les pieds de la Femme pendant 2 minutes. Tags: #massage #softcore Hot: 1
12.	Femme : Fais un lapdance habillée sur l’Homme pendant 90 secondes. Tags: #lapdance #grinding #softcore Hot: 2
13.	Homme : Caresse le ventre et l’intérieur des cuisses de la Femme par-dessus ses vêtements pendant 75 secondes. Tags: #teasing #caresses #softcore Hot: 1
14.	Femme : Embrasse l’Homme avec un french kiss profond pendant 75 secondes. Tags: #baiser #softcore Hot: 1
15.	Homme : Utilise le masse-tête sur le dos et les fesses de la Femme pendant 2 minutes. Tags: #massage #softcore Hot: 1
16.	Femme : Bois un cocktail entier. Tags: #alcool Hot: 1
17.	Homme : Embrasse le ventre de la Femme en descendant lentement pendant 60 secondes. Tags: #baiser #teasing #softcore Hot: 2
18.	Femme : Caresse le sexe de l’Homme par-dessus son pantalon pendant 75 secondes. Tags: #teasing #caresses #softcore Hot: 2
19.	Homme : Bande les yeux de la Femme et caresse son visage et son cou pendant 90 secondes. Tags: #bandeau #sensuel #softcore Hot: 1
20.	Femme : Assieds-toi dos contre l’Homme et frotte-toi doucement contre lui pendant 90 secondes. Tags: #grinding #teasing #softcore Hot: 2
21.	Homme : Caresse les cheveux et le dos de la Femme pendant 2 minutes. Tags: #caresses #sensuel #softcore Hot: 1
22.	Femme : Embrasse le torse de l’Homme tout en caressant ses bras pendant 75 secondes. Tags: #baiser #caresses #softcore Hot: 2
23.	Homme : Bois une gorgée de gin ou de cocktail. Tags: #alcool Hot: 1
24.	Femme : Danse sensuellement contre le corps de l’Homme pendant 90 secondes. Tags: #striptease #teasing #softcore Hot: 2
25.	Homme : Caresse les seins de la Femme par-dessus ses vêtements pendant 75 secondes. Tags: #seins #caresses #softcore Hot: 2
26.	Femme : Lèche lentement les lèvres et le cou de l’Homme. Tags: #baiser #softcore Hot: 1
27.	Homme : Massage les cuisses de la Femme pendant 2 minutes. Tags: #massage #teasing #softcore Hot: 1
28.	Femme : Frotte ta poitrine contre le torse de l’Homme pendant 90 secondes. Tags: #grinding #teasing #softcore Hot: 2
29.	Homme : Bande les yeux de la Femme et caresse ses bras et jambes avec la plume. Tags: #bandeau #plume #softcore Hot: 1
30.	Femme : Fais un massage de la tête et des tempes de l’Homme pendant 90 secondes. Tags: #massage #softcore Hot: 1
31.	Homme : Caresse les fesses de la Femme par-dessus ses vêtements pendant 90 secondes. Tags: #teasing #caresses #softcore Hot: 2
32.	Femme : Embrasse et mordille doucement les oreilles de l’Homme. Tags: #baiser #softcore Hot: 2
33.	Homme : Bois la moitié d’une bière. Tags: #alcool Hot: 1
34.	Femme : Caresse le torse de l’Homme avec tes ongles doucement pendant 75 secondes. Tags: #caresses #teasing #softcore Hot: 2
35.	Homme : Embrasse les mains et les poignets de la Femme. Tags: #baiser #softcore Hot: 1
36.	Femme : Assieds-toi sur les genoux de l’Homme et frotte-toi légèrement contre lui. Tags: #grinding #softcore Hot: 2
37.	Homme : Massage les épaules de la Femme avec de l’huile. Tags: #massage #huile #softcore Hot: 1
38.	Femme : Réalise un strip-tease lent d’un seul accessoire. Tags: #striptease #softcore Hot: 1
39.	Homme : Caresse le dos de la Femme sous ses vêtements. Tags: #caresses #softcore Hot: 2
40.	Femme : Embrasse l’Homme avec un french kiss tout en caressant sa nuque. Tags: #baiser #softcore Hot: 2

PHASE 2 – Déshabillage & Sensualité Peau à Peau (Hot 2-3)
1.	Homme : Enlève le haut de la Femme et masse ses seins nus pendant 2 minutes. Tags: #seins #caresses #déshabillage #softcore Hot: 2
2.	Femme : Fais une fellation lente et nue à l’Homme pendant 2 minutes. Tags: #oral #fellation #softcore Hot: 3
3.	Homme : Caresse le clitoris de la Femme avec tes doigts par-dessus sa culotte pendant 2 minutes. Tags: #doigts #clito #teasing #masturbation #softcore Hot: 3
4.	Femme : Réalise un strip-tease complet jusqu’à rester en lingerie. Tags: #striptease #déshabillage #softcore Hot: 2
5.	Homme : Lèche les tétons de la Femme pendant 90 secondes. Tags: #oral #seins #softcore Hot: 3
6.	Femme : Fais un massage érotique du dos et des fesses de l’Homme avec de l’huile. Tags: #massage #huile #softcore Hot: 2
7.	Homme : Insère les boules de geisha à la Femme et fais-la marcher pendant 90 secondes. Tags: #jouet #teasing #softcore Hot: 3
8.	Femme : Lèche les testicules et le périnée de l’Homme pendant 2 minutes. Tags: #oral #softcore Hot: 3
9.	Homme : Bois les deux tiers d’une bière. Tags: #alcool Hot: 2
10.	Femme : Chevauche l’Homme nue avec seulement un frottement extérieur pendant 3 minutes. Tags: #grinding #teasing #softcore Hot: 3
11.	Homme : Caresse tout le corps nu de la Femme avec la plume pendant 3 minutes. Tags: #plume #teasing #softcore Hot: 2
12.	Femme : Faites un 69 léger avec seulement des baisers et caresses pendant 2 minutes. Tags: #69 #oral #softcore Hot: 3
13.	Homme : Stimule le clitoris de la Femme avec tes doigts pendant 3 minutes. Tags: #doigts #clito #masturbation #softcore Hot: 3
14.	Femme : Lèche les tétons de l’Homme tout en le branlant doucement. Tags: #oral #doigts #masturbation #softcore Hot: 3
15.	Homme : Enlève la culotte de la Femme avec tes dents. Tags: #striptease #teasing #softcore Hot: 2
16.	Femme : Bois un cocktail entier. Tags: #alcool Hot: 2
17.	Homme : Massage le périnée de l’Homme pendant 2 minutes. Tags: #teasing #softcore Hot: 3
18.	Femme : Fais un titjob avec tes seins sur le sexe de l’Homme pendant 2 minutes. Tags: #titjob #teasing #softcore Hot: 3
19.	Homme : Bande les yeux de la Femme, utilise la plume et tes doigts sur son corps. Tags: #bandeau #plume #doigts #softcore Hot: 3
20.	Femme : Fais un lapdance complètement nue sur l’Homme pendant 3 minutes. Tags: #lapdance #grinding #softcore Hot: 3
21.	Homme : Caresse tout le corps nu de la Femme pendant 3 minutes. Tags: #caresses #sensuel #softcore Hot: 2
22.	Femme : Fais une fellation à l’Homme les yeux bandés pendant 2 minutes. Tags: #oral #fellation #bandeau #softcore Hot: 3
23.	Homme : Stimule les seins et les tétons de la Femme pendant 3 minutes. Tags: #seins #caresses #softcore Hot: 3
24.	Femme : Caresse le sexe de l’Homme avec du lubrifiant pendant 2 minutes. Tags: #lubrifiant #doigts #masturbation #softcore Hot: 3
25.	Homme : Bois un shot de gin ou de cocktail. Tags: #alcool Hot: 2
26.	Femme : Frotte ton clitoris contre la cuisse de l’Homme. Tags: #grinding #masturbation #teasing #softcore Hot: 3
27.	Homme : Lèche le ventre et les hanches de la Femme. Tags: #oral #teasing #softcore Hot: 2
28.	Femme : Massage les testicules de l’Homme pendant 2 minutes. Tags: #caresses #softcore Hot: 3
29.	Homme : Bande les yeux de la Femme et caresse l’intérieur de ses cuisses. Tags: #bandeau #teasing #softcore Hot: 3
30.	Femme : Chevauche l’Homme en lingerie pendant 3 minutes. Tags: #grinding #softcore Hot: 3
31.	Homme : Caresse les fesses nues de la Femme. Tags: #caresses #softcore Hot: 3
32.	Femme : Lèche le périnée et les testicules de l’Homme. Tags: #oral #softcore Hot: 3
33.	Homme : Caresse l’anus externe de la Femme pendant 2 minutes. Tags: #anal #prep #softcore Hot: 3
34.	Femme : Branle l’Homme lentement pendant 2 minutes. Tags: #doigts #masturbation #softcore Hot: 3
35.	Homme : Fais un massage complet du corps de la Femme avec de l’huile. Tags: #massage #huile #softcore Hot: 2
36.	Femme : Embrasse l’Homme profondément tout en caressant son sexe. Tags: #baiser #teasing #softcore Hot: 3
37.	Homme : Stimule le clitoris de la Femme avec la plume. Tags: #plume #clito #masturbation #softcore Hot: 3
38.	Femme : Retiens ton excitation pendant 1 minute (edging). Tags: #edging #rétention #softcore Hot: 3
39.	Homme : Caresse doucement l’anus de la Femme. Tags: #anal #prep #softcore Hot: 3
40.	Femme : Fais un lapdance accompagné de baisers profonds. Tags: #lapdance #baiser #softcore Hot: 3

PHASE 3 – Excitation Orale & Jouets (Hot 3-4)
1.	Homme : Fais un cunnilingus à la Femme pendant 4 minutes. Tags: #oral #cunnilingus #softcore Hot: 4
2.	Femme : Fais une fellation profonde à l’Homme pendant 4 minutes. Tags: #oral #fellation #softcore Hot: 4
3.	Homme : Utilise le rabbit vibrator sur le clitoris de la Femme pendant 4 minutes. Tags: #jouet #vibration #clito #masturbation #softcore Hot: 4
4.	Femme : Suce l’Homme tout en portant les boules de geisha. Tags: #oral #jouet #softcore Hot: 4
5.	Homme : Combine doigts et cunnilingus pendant 4 minutes. Tags: #doigts #oral #softcore Hot: 4
6.	Femme : Fais un deepthroat pendant 3 minutes. Tags: #oral #fellation #softcore Hot: 4
7.	Homme : Insère lentement le plug anal à la Femme avec beaucoup de lubrifiant pendant 3 minutes. Tags: #anal #plug #lubrifiant #prep #softcore Hot: 4
8.	Femme : Branle l’Homme tout en léchant partout pendant 4 minutes. Tags: #doigts #oral #masturbation #softcore Hot: 4
9.	Homme : Bois un shot de cocktail. Tags: #alcool Hot: 3
10.	Femme : Faites un 69 complet pendant 5 minutes. Tags: #69 #oral #softcore Hot: 4
11.	Homme : Utilise le rabbit tout en léchant les seins de la Femme. Tags: #jouet #oral #softcore Hot: 4
12.	Femme : Fais une fellation avec les boules de geisha en toi. Tags: #oral #jouet #softcore Hot: 4
13.	Homme : Insère doucement un doigt anal avec lubrifiant pendant 4 minutes. Tags: #anal #prep #lubrifiant #softcore Hot: 4
14.	Femme : Lèche tout le corps de l’Homme en descendant lentement. Tags: #oral #softcore Hot: 4
15.	Homme : Contrôle le rabbit sur la Femme pendant 5 minutes. Tags: #jouet #teasing #softcore Hot: 4
16.	Femme : Fais une fellation intense pendant 4 minutes. Tags: #oral #fellation #softcore Hot: 4
17.	Homme : Combine plug anal et stimulation du clito. Tags: #anal #jouet #softcore Hot: 4
18.	Femme : Bois un cocktail entier. Tags: #alcool Hot: 3
19.	Homme : Combine cunnilingus et rabbit. Tags: #oral #jouet #softcore Hot: 4
20.	Femme : Fais une fellation tout en massant le périnée. Tags: #oral #teasing #softcore Hot: 4
21.	Homme : Stimule le vagin et le clito avec tes doigts pendant 4 minutes. Tags: #doigts #masturbation #softcore Hot: 4
22.	Femme : Suce l’Homme en chevauchant son visage. Tags: #69 #oral #softcore Hot: 4
23.	Homme : Fais de l’edging à la Femme pendant 3 minutes. Tags: #edging #rétention #masturbation #softcore Hot: 4
24.	Femme : Fais un titjob intense pendant 3 minutes. Tags: #titjob #softcore Hot: 4
25.	Homme : Utilise le plug anal avec vibrations. Tags: #anal #jouet #softcore Hot: 4
26.	Femme : Fais un deepthroat en regardant l’Homme dans les yeux. Tags: #oral #softcore Hot: 4
27.	Homme : Fais un cunnilingus intense. Tags: #oral #softcore Hot: 4
28.	Femme : Alterne branlette rapide et lente (edging). Tags: #doigts #masturbation #edging #softcore Hot: 4
29.	Homme : Applique du lubrifiant et caresse analement. Tags: #anal #lubrifiant #softcore Hot: 4
30.	Femme : Faites un 69 avec le rabbit. Tags: #69 #jouet #softcore Hot: 4
31.	Homme : Contrôle le rythme de la fellation de la Femme. Tags: #oral #teasing #softcore Hot: 4
32.	Femme : Retiens ton orgasme pendant 2 minutes (edging). Tags: #edging #rétention #softcore Hot: 4
33.	Homme : Utilise plusieurs jouets en même temps. Tags: #jouet #softcore Hot: 4
34.	Femme : Fais une fellation en caressant les testicules. Tags: #oral #softcore Hot: 4
35.	Homme : Combine doigts et plug anal. Tags: #doigts #anal #softcore Hot: 4
36.	Femme : Lèche tout le corps de l’Homme très lentement. Tags: #oral #slow #softcore Hot: 4
37.	Homme : Contrôle totalement le rabbit sur la Femme. Tags: #jouet #teasing #softcore Hot: 4
38.	Femme : Fais un oral tout en faisant de l’edging à l’Homme. Tags: #oral #edging #softcore Hot: 4
39.	Homme : Fais une préparation anale avancée. Tags: #anal #prep #softcore Hot: 4
40.	Femme : Fais une fellation tout en caressant tes seins. Tags: #oral #seins #softcore Hot: 4

PHASE 4 – Intensité & Préparation Anale (Hot 4-5)
1.	Homme : Pénètre vaginalement la Femme lentement pendant 6 minutes. Tags: #pénétration #sexe #slow #softcore Hot: 4
2.	Femme : Chevauche l’Homme en gardant le contrôle total pendant 6 minutes. Tags: #sexe #cowgirl #softcore Hot: 5
3.	Homme : Alterne pénétration vaginale et plug anal. Tags: #pénétration #anal #softcore Hot: 5
4.	Femme : Laisse l’Homme te prendre en missionnaire profonde pendant 6 minutes. Tags: #pénétration #missionnaire #softcore Hot: 5
5.	Homme : Combine cunnilingus, doigts et plug anal. Tags: #oral #anal #softcore Hot: 4
6.	Femme : Fais une fellation très intense pendant 5 minutes. Tags: #oral #softcore Hot: 4
7.	Homme : Prends la Femme en levrette pendant 6 minutes. Tags: #pénétration #levrette #softcore Hot: 5
8.	Femme : Utilise le rabbit sur toi pendant que tu suces l’Homme. Tags: #jouet #oral #softcore Hot: 4
9.	Homme : Tente une pénétration anale très lente et préparée. Tags: #anal #softcore Hot: 5
10.	Femme : Bois un grand verre de cocktail. Tags: #alcool Hot: 4
11.	Homme : Baise la Femme fermement sans douleur. Tags: #sexe #intense #hardcore #softcore Hot: 5
12.	Femme : Chevauche l’Homme avec le plug anal. Tags: #sexe #anal #softcore Hot: 5
13.	Homme : Faites un 69 très intense. Tags: #69 #oral #softcore Hot: 4
14.	Femme : Prends la position amazone pendant 6 minutes. Tags: #sexe #softcore Hot: 5
15.	Homme : Utilise tous les jouets en même temps sur la Femme. Tags: #jouet #softcore Hot: 4
16.	Femme : Fais une fellation et avale si tu le désires. Tags: #oral #softcore Hot: 5
17.	Homme : Combine pénétration et stimulation anale. Tags: #pénétration #anal #softcore Hot: 5
18.	Femme : Laisse l’Homme te prendre comme il veut pendant 7 minutes. Tags: #sexe #intense #hardcore #softcore Hot: 5
19.	Homme : Porte le plug anal pendant que tu pénètres la Femme. Tags: #anal #sexe #softcore Hot: 5
20.	Femme : Fais de l’edging à l’Homme pendant 4 minutes. Tags: #edging #rétention #softcore Hot: 5
21.	Homme : Prends la Femme en position cuillères profondes. Tags: #pénétration #softcore Hot: 5
22.	Femme : Contrôle ton propre orgasme (edging). Tags: #edging #rétention #masturbation #softcore Hot: 5
23.	Homme : Prends la Femme en levrette avec le rabbit. Tags: #pénétration #jouet #softcore Hot: 5
24.	Femme : Chevauche l’Homme de façon intense. Tags: #sexe #hardcore #softcore Hot: 5
25.	Homme : Combine anal play et pénétration vaginale. Tags: #anal #pénétration #softcore Hot: 5
26.	Femme : Continue la fellation jusqu’au bout. Tags: #oral #softcore Hot: 5
27.	Homme : Missionnaire avec les jambes de la Femme sur tes épaules. Tags: #pénétration #softcore Hot: 5
28.	Femme : Retiens ton plaisir pendant 3 minutes. Tags: #edging #rétention #softcore Hot: 5
29.	Homme : Pénètre la Femme debout. Tags: #sexe #softcore Hot: 5
30.	Femme : Utilise les jouets sur l’Homme. Tags: #jouet #softcore Hot: 4
31.	Homme : Réalise une pénétration anale complète très lente si accepté. Tags: #anal #softcore Hot: 5
32.	Femme : Sexe oral mutuel très intense. Tags: #69 #oral #softcore Hot: 5
33.	Homme : Pénètre avec beaucoup de lubrifiant. Tags: #pénétration #lubrifiant #softcore Hot: 5
34.	Femme : Laisse-toi complètement aller. Tags: #sexe #intense #hardcore #softcore Hot: 5
35.	Homme : Contrôle l’orgasme de la Femme. Tags: #edging #softcore Hot: 5
36.	Femme : Chevauche l’Homme tout en l’embrassant. Tags: #sexe #cowgirl #softcore Hot: 5
37.	Homme : Prends la Femme en levrette avec un léger hairpulling consensuel. Tags: #pénétration #hairpulling #softcore Hot: 5
38.	Femme : Combine plusieurs jouets et oral. Tags: #jouet #oral #softcore Hot: 5
39.	Homme : Pénètre lentement avec beaucoup de teasing. Tags: #pénétration #teasing #softcore Hot: 5
40.	Femme : Prends le contrôle total pendant 7 minutes. Tags: #sexe #softcore Hot: 5

PHASE 5 – Sexe Libre & Climax (Hot 5)
1.	Homme : Baise la Femme dans ta position préférée pendant 8 à 10 minutes. Tags: #pénétration #sexe #hardcore #softcore Hot: 5
2.	Femme : Chevauche l’Homme jusqu’à ce qu’il jouisse. Tags: #sexe #cowgirl #softcore Hot: 5
3.	Homme : Prends la Femme en levrette profonde pendant 8 minutes. Tags: #pénétration #levrette #hardcore #softcore Hot: 5
4.	Femme : Fais une fellation et avale. Tags: #oral #softcore Hot: 5
5.	Homme : Pénètre la Femme tout en utilisant le plug anal sur elle. Tags: #pénétration #anal #softcore Hot: 5
6.	Femme : Laisse l’Homme te prendre de façon intense et consentie. Tags: #sexe #intense #hardcore #softcore Hot: 5
7.	Homme : Faites un sexe oral mutuel très intense. Tags: #69 #oral #softcore Hot: 5
8.	Femme : Atteins plusieurs orgasmes avec le rabbit et l’Homme. Tags: #jouet #masturbation #softcore Hot: 5
9.	Homme : Réalise une pénétration anale complète si accepté. Tags: #anal #softcore Hot: 5
10.	Femme : Bois un dernier verre puis baise l’Homme comme tu veux. Tags: #alcool #sexe #softcore Hot: 5
11.	Homme : Prends la Femme en missionnaire avec les jambes relevées. Tags: #pénétration #missionnaire #softcore Hot: 5
12.	Femme : Masturbe l’Homme jusqu’à l’orgasme avec ta bouche et tes mains. Tags: #masturbation #oral #softcore Hot: 5
13.	Homme : Baise la Femme debout contre un mur. Tags: #sexe #hardcore #softcore Hot: 5
14.	Femme : Chevauche l’Homme en amazone intense. Tags: #sexe #softcore Hot: 5
15.	Homme : Combine pénétration et stimulation du clito avec le rabbit. Tags: #pénétration #jouet #softcore Hot: 5
16.	Femme : Laisse l’Homme te prendre en cuillères tout en te caressant. Tags: #sexe #softcore Hot: 5
17.	Homme : Fais de l’edging à la Femme avant de la pénétrer. Tags: #edging #pénétration #softcore Hot: 5
18.	Femme : Masturbe-toi devant l’Homme puis laisse-le te prendre. Tags: #masturbation #teasing #softcore Hot: 5
19.	Homme : Prends la Femme en levrette avec léger hairpulling. Tags: #pénétration #hairpulling #hardcore #softcore Hot: 5
20.	Femme : Contrôle le rythme et fais jouir l’Homme comme tu veux. Tags: #sexe #softcore Hot: 5
21.	Homme : Pénètre la Femme tout en utilisant le plug anal et le rabbit. Tags: #pénétration #anal #jouet #softcore Hot: 5
22.	Femme : Fais une fellation très profonde jusqu’à la fin. Tags: #oral #softcore Hot: 5
23.	Homme : Baise la Femme en missionnaire en la regardant dans les yeux. Tags: #pénétration #missionnaire #softcore Hot: 5
24.	Femme : Retiens ton orgasme le plus longtemps possible puis lâche-toi. Tags: #edging #rétention #softcore Hot: 5
25.	Homme : Prends la Femme par derrière avec beaucoup de lubrifiant. Tags: #pénétration #lubrifiant #softcore Hot: 5
26.	Femme : Utilise tous les jouets sur toi pendant que l’Homme te regarde. Tags: #jouet #masturbation #softcore Hot: 5
27.	Homme : Alterne pénétration vaginale et anal play. Tags: #pénétration #anal #softcore Hot: 5
28.	Femme : Chevauche l’Homme jusqu’à ce que vous jouissiez ensemble. Tags: #sexe #cowgirl #softcore Hot: 5
29.	Homme : Baise la Femme de façon intense et passionnée. Tags: #sexe #hardcore #softcore Hot: 5
30.	Femme : Masturbe l’Homme avec tes seins et ta bouche. Tags: #titjob #oral #masturbation #softcore Hot: 5
31.	Homme : Prends la Femme en position debout ou contre un meuble. Tags: #sexe #softcore Hot: 5
32.	Femme : Laisse l’Homme te doigter et te lécher jusqu’à l’orgasme. Tags: #doigts #oral #softcore Hot: 5
33.	Homme : Pénètre lentement puis accélère progressivement. Tags: #pénétration #teasing #softcore Hot: 5
34.	Femme : Prends le contrôle total et baise l’Homme comme tu le désires. Tags: #sexe #softcore Hot: 5
35.	Homme : Combine tous les jouets et la pénétration. Tags: #jouet #pénétration #softcore Hot: 5
36.	Femme : Fais un 69 intense jusqu’à l’orgasme mutuel. Tags: #69 #oral #softcore Hot: 5
37.	Homme : Baise la Femme en cuillères tout en stimulant son clito. Tags: #pénétration #clito #softcore Hot: 5
38.	Femme : Masturbe-toi sur le sexe de l’Homme avant la pénétration. Tags: #masturbation #teasing #softcore Hot: 5
39.	Homme : Prends la Femme comme tu veux pour le final. Tags: #sexe #hardcore #softcore Hot: 5
40.	Femme : Laisse-toi aller complètement et jouis plusieurs fois. Tags: #sexe #softcore Hot: 5
"""

def parse_gages(text):
    gages = []
    current_phase = 0
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Phase header
        phase_match = re.match(r'PHASE (\d+)', line)
        if phase_match:
            current_phase = int(phase_match.group(1))
            continue
            
        # Gage line
        gage_match = re.match(r'(\d+)\.\s+(Homme|Femme)\s*:\s*(.*?)Tags:\s*(.*?)\s+Hot:\s*(\d+)', line)
        if gage_match:
            id_in_phase = int(gage_match.group(1))
            target = gage_match.group(2)
            description = gage_match.group(3).strip()
            tags_str = gage_match.group(4).strip()
            hot = int(gage_match.group(5))
            
            # Robust tag extraction
            tags = []
            # Split by space or comma, then clean
            for part in re.split(r'[ ,]+', tags_str):
                clean_tag = part.replace('#', '').strip()
                if clean_tag:
                    tags.append(clean_tag)
            
            # Duration extraction
            duration = 0
            sec_match = re.search(r'pendant (\d+)\s*secondes?', description, re.IGNORECASE)
            if sec_match:
                duration = int(sec_match.group(1))
            else:
                min_match = re.search(r'pendant (\d+)\s*minutes?', description, re.IGNORECASE)
                if min_match:
                    duration = int(min_match.group(1)) * 60
                else:
                    range_match = re.search(r'pendant (\d+)\s*à\s*(\d+)\s*minutes?', description, re.IGNORECASE)
                    if range_match:
                        duration = int(range_match.group(1)) * 60
            
            gages.append({
                "id": len(gages) + 1,
                "phase": current_phase,
                "target": target,
                "text": description,
                "tags": tags,
                "hot": hot,
                "duration": duration
            })
            
    return gages

all_gages = parse_gages(gages_text)
with open('data/gages.json', 'w', encoding='utf-8') as f:
    json.dump(all_gages, f, ensure_ascii=False, indent=2)

print(f"Parsed {len(all_gages)} gages.")

```

# FILE: scripts\reorganize_json.py
```py
import json
import os
import re

path = 'data/gages.json'
if not os.path.exists(path):
    print(f"File {path} not found.")
    exit(1)

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Nettoyage préventif des erreurs de syntaxe JSON courantes
content = re.sub(r'\}\s*\{', '},\n  {', content) # Virgules manquantes
content = re.sub(r',(\s*[\]\}])', r'\1', content) # Virgules traînantes
content = re.sub(r'//.*', '', content) # Supprimer les anciens commentaires

try:
    gages = json.loads(content)
except Exception as e:
    print(f"Error parsing JSON: {e}")
    exit(1)

# Tri par phase puis par hotness
gages.sort(key=lambda x: (int(x.get('phase', 0)), int(x.get('hot', 0))))

# Réattribution des IDs
for i, g in enumerate(gages):
    g['id'] = i + 1

# Groupement par phase pour l'insertion des commentaires
phases = {}
for g in gages:
    p = g.get('phase', 0)
    if p not in phases:
        phases[p] = []
    phases[p].append(g)

# Construction manuelle du fichier JSON avec commentaires
output = ["[\n"]
sorted_phases = sorted(phases.keys())
max_p = sorted_phases[-1] if sorted_phases else 0

for p in sorted_phases:
    output.append(f"  // ==========================================\n")
    output.append(f"  // PHASE {p}\n")
    output.append(f"  // ==========================================\n")
    
    phase_gages = phases[p]
    for i, gage in enumerate(phase_gages):
        gage_str = json.dumps(gage, ensure_ascii=False, indent=2)
        # Indentation pour le fichier final
        indented = "\n".join("  " + line for line in gage_str.split("\n"))
        output.append(indented)
        
        # Virgule sauf pour le tout dernier élément absolu
        if not (p == max_p and i == len(phase_gages) - 1):
            output.append(",")
        output.append("\n")

output.append("]")

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(output)

print(f"Successfully reorganized {len(gages)} gages with phase comments.")

```

# FILE: utils\engine.py
```py
import json
import random

class GameEngine:
    def __init__(self, gages_path='data/gages.json'):
        with open(gages_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Supprimer les commentaires // avant de parser le JSON
            import re
            content = re.sub(r'//.*', '', content)
            self.all_gages = json.loads(content)
            
    def filter_gages(self, accepted_tags):
        """Filtre les gages selon les tags acceptés."""
        filtered = []
        for gage in self.all_gages:
            # Un gage est accepté si TOUS ses tags sont dans la liste des tags acceptés
            if all(tag in accepted_tags for tag in gage['tags']):
                filtered.append(gage)
        return filtered

    def get_next_gage(self, current_phase, next_player, history, accepted_tags):
        """Sélectionne le prochain gage avec une montée progressive du niveau Hot."""
        # 1. Filtrage par tags et phase et genre
        available = [g for g in self.filter_gages(accepted_tags) 
                     if g['phase'] == current_phase 
                     and g['target'] == next_player
                     and g['id'] not in history]
        
        if not available:
            return None
            
        # 2. Montée progressive (Hot Smoothing)
        # On trie par niveau Hot
        available.sort(key=lambda x: x['hot'])
        
        # On définit une fenêtre de sélection basée sur la progression dans la phase
        # Si on a déjà fait beaucoup de gages dans cette phase, on pioche plus haut
        gages_done_in_phase = len([h for h in history if any(g['id'] == h and g['phase'] == current_phase for g in self.all_gages)])
        
        # Facteur de progression (0.0 à 1.0)
        # On suppose une dizaine de gages par phase en moyenne
        progression = min(gages_done_in_phase / 10.0, 1.0)
        
        # On prend une sous-liste qui s'élargit vers le haut
        # Au début (progression=0), on prend les 40% les plus bas
        # À la fin (progression=1), on prend toute la liste
        window_size = int(len(available) * (0.4 + 0.6 * progression))
        window_size = max(window_size, 1)
        
        selection_pool = available[:window_size]
        
        # On pioche au hasard dans le pool restreint
        return random.choice(selection_pool)

    def get_drink_suggestion(self):
        """Retourne une suggestion de boisson douce."""
        suggestions = [
            "Prenez une petite gorgée de votre boisson préférée ensemble.",
            "L'un de vous doit servir une gorgée à l'autre.",
            "Trinquez à votre complicité et buvez une gorgée.",
            "Une petite pause fraîcheur ? Une gorgée pour chacun.",
            "L'Homme embrasse la Femme, puis les deux boivent une gorgée."
        ]
        return random.choice(suggestions)

```

# FILE: utils\state.py
```py
import streamlit as st
import time

def init_state():
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = 1
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'next_player' not in st.session_state:
        st.session_state.next_player = "Homme"
    if 'current_gage' not in st.session_state:
        st.session_state.current_gage = None
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'drink_counter' not in st.session_state:
        st.session_state.drink_counter = 0
    if 'total_gages_target' not in st.session_state:
        st.session_state.total_gages_target = 30
    if 'phase_distribution' not in st.session_state:
        st.session_state.phase_distribution = {1: 10, 2: 8, 3: 6, 4: 4, 5: 2}
    if 'total_done' not in st.session_state:
        st.session_state.total_done = 0
    if 'names' not in st.session_state:
        st.session_state.names = {"Homme": "Iz", "Femme": "Fa"}
    if 'accepted_tags' not in st.session_state:
        st.session_state.accepted_tags = []
    if 'sex_finality' not in st.session_state:
        st.session_state.sex_finality = True
    if 'gages_in_current_phase' not in st.session_state:
        st.session_state.gages_in_current_phase = 0
    if 'timer_active' not in st.session_state:
        st.session_state.timer_active = False
    if 'timer_seconds' not in st.session_state:
        st.session_state.timer_seconds = 0
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False

def get_elapsed_time():
    if st.session_state.start_time:
        return int((time.time() - st.session_state.start_time) / 60)
    return 0

def get_progress():
    if st.session_state.get('total_gages_target', 0) > 0:
        return st.session_state.total_done / st.session_state.total_gages_target
    return 0

```

# FILE: utils\__init__.py
```py

```

# FILE: utils\__pycache__\engine.cpython-312.pyc
Binary file
Size: 3715 bytes
SHA256: e497414e77e07f7de976ae4fc34b3a321a17c3add4831e85598324e2ef48a7b8

# FILE: utils\__pycache__\engine.cpython-314.pyc
Binary file
Size: 4346 bytes
SHA256: c4ac836b33328364a163219cb75e4f93abf346f58912d4c0004d8d90b6d337fa

# FILE: utils\__pycache__\state.cpython-312.pyc
Binary file
Size: 3332 bytes
SHA256: 85adc7754cec7af9564814fb75644c908770963f176e558eb64d96dcacdee7c1

# FILE: utils\__pycache__\state.cpython-314.pyc
Binary file
Size: 3427 bytes
SHA256: 5e68b7ac796b99c50e4e7db3d4001704f2186885ef0239fa934432b9ece03ba0

# FILE: assets\sounds\success.mp3
Binary file
Size: 29291 bytes
SHA256: ef3f15ee6e4437e6221c8114fb46db3a080f1f7df5cd2cbadc6e299f619f8a60
