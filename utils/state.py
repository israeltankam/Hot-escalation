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
