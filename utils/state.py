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
    if 'total_duration' not in st.session_state:
        st.session_state.total_duration = 60 # minutes
    if 'names' not in st.session_state:
        st.session_state.names = {"Homme": "Iz", "Femme": "Fa"}
    if 'accepted_tags' not in st.session_state:
        st.session_state.accepted_tags = []
    if 'sex_finality' not in st.session_state:
        st.session_state.sex_finality = True
    if 'gages_in_current_phase' not in st.session_state:
        st.session_state.gages_in_current_phase = 0

def get_elapsed_time():
    if st.session_state.start_time:
        return int((time.time() - st.session_state.start_time) / 60)
    return 0

def get_remaining_time():
    elapsed = get_elapsed_time()
    return max(st.session_state.total_duration - elapsed, 0)
