import streamlit as st
import time
import random
from utils.engine import GameEngine
from utils.state import init_state, get_elapsed_time, get_remaining_time

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
    
    # Logic pour changement de phase automatique
    # Proportionnel à la durée : ex: 10 gages par phase pour 60 min
    gages_per_phase = max(st.session_state.total_duration // 6, 5)
    
    if st.session_state.gages_in_current_phase >= gages_per_phase:
        if st.session_state.current_phase < 5:
            if st.session_state.current_phase == 4 and not st.session_state.sex_finality:
                pass # Stay in phase 4 if no sex finality
            else:
                st.session_state.current_phase += 1
                st.session_state.gages_in_current_phase = 0
    
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

# --- SAFE WORD ---
st.markdown('<div class="safe-word">', unsafe_allow_html=True)
if st.button("STOP", key="stop_btn"):
    st.session_state.game_started = False
    st.session_state.current_gage = None
    st.rerun()
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
if not st.session_state.game_started:
    st.title("🔥 Hot Escalation")
    st.markdown("### Préparez votre soirée...")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.names["Homme"] = st.text_input("Prénom Lui", value="Iz")
    with col2:
        st.session_state.names["Femme"] = st.text_input("Prénom Elle", value="Fa")
        
    st.markdown("---")
    
    all_tags = ['69', 'alcool', 'anal', 'baiser', 'bandeau', 'caresses', 'clito', 'cowgirl', 'cunnilingus', 'doigts', 'déshabillage', 'edging', 'fellation', 'grinding', 'hairpulling', 'hardcore', 'huile', 'intense', 'jouet', 'lapdance', 'levrette', 'lubrifiant', 'massage', 'masturbation', 'missionnaire', 'oral', 'plug', 'plume', 'prep', 'pénétration', 'rétention', 'seins', 'sensuel', 'sexe', 'slow', 'softcore', 'striptease', 'teasing', 'titjob', 'vibration']
    
    st.markdown("#### Tags acceptés")
    st.session_state.accepted_tags = st.multiselect(
        "Cochez ce que vous acceptez ce soir :",
        options=all_tags,
        default=['baiser', 'sensuel', 'slow', 'softcore', 'massage', 'caresses', 'teasing', 'seins', 'oral', 'fellation', 'alcool']
    )
    
    col3, col4 = st.columns(2)
    with col3:
        duration_label = st.select_slider(
            "Durée du jeu",
            options=["1h", "1h30", "2h", "3h"],
            value="1h"
        )
        durations = {"1h": 60, "1h30": 90, "2h": 120, "3h": 180}
        st.session_state.total_duration = durations[duration_label]
        
    with col4:
        st.session_state.sex_finality = st.toggle("Finalité Sexe", value=True)
        
    if st.button("COMMENCER L'ASCENSION"):
        if not st.session_state.accepted_tags:
            st.error("Veuillez choisir au moins quelques tags.")
        else:
            st.session_state.game_started = True
            st.session_state.start_time = time.time()
            st.session_state.current_gage = engine.get_next_gage(
                st.session_state.current_phase,
                st.session_state.next_player,
                st.session_state.history,
                st.session_state.accepted_tags
            )
            st.rerun()

# --- GAME SCREEN ---
else:
    # Header Info
    elapsed = get_elapsed_time()
    remaining = get_remaining_time()
    
    st.markdown(f'<div class="phase-info">Phase {st.session_state.current_phase} • {elapsed}m écoulés / {remaining}m restants</div>', unsafe_allow_html=True)
    st.progress(elapsed / st.session_state.total_duration if st.session_state.total_duration > 0 else 0)
    
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
        if st.session_state.drink_counter >= 3:
            if random.random() > 0.5: # 50% de chance après 3 gages
                st.markdown(f'<div class="drink-suggestion">🍹 {engine.get_drink_suggestion()}</div>', unsafe_allow_html=True)
                st.session_state.drink_counter = 0

        # Buttons
        col_a, col_b = st.columns([3, 1])
        with col_a:
            if st.button("SUIVANT"):
                next_turn()
                st.rerun()
        with col_b:
            if st.button("PASSER"):
                skip_turn()
                st.rerun()
                
    else:
        st.markdown("""
        <div class="gage-card">
            <div class="gage-text">Plus de gages disponibles avec vos filtres dans cette phase.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("PASSER À LA PHASE SUIVANTE"):
            st.session_state.current_phase += 1
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
