import streamlit as st
import sqlite3

import data_processing as d_p
import database_connection as d_c

st.set_page_config(
    page_title="Durak",
    page_icon="🃏",
)

hide_menu = """
<style>
#MainMenu {visibility:hidden;}
footer{visibility:hidden;}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)

st.markdown("""
<style>
.small-font-green {
    font-size:12px;
    color: green;
}
.small-font-red {
    font-size:12px;
    color: red;
}
.normal-font-red {
    font-size:16px;
    color: red;
}
.normal-font-green {
    font-size:16px;
    color: green;
}
</style>""", unsafe_allow_html=True)

st.title("Start")

from streamlit_option_menu import option_menu

#with st.sidebar:
#    selected = option_menu("DURAK", ["Home", 'Einstellungen'],
#        icons=['house', 'gear'], menu_icon="cast", default_index=1)


@st.experimental_singleton
def init_connection():
    return sqlite3.connect("database/durak_db")


is_open, session_id, start_time, player_ingame = d_c.check_session_open()

if is_open:
    current_players = d_c.return_sessions_table().loc[session_id].Fellow_Players
    current_players = current_players.replace("[", "")
    current_players = current_players.replace("]", "")
    current_players = current_players.replace(" ", "")
    current_players = current_players.replace("'", "")

    current_players = current_players.split(",")

    game_number, last_winner, last_looser = d_c.return_last_game_results(session_id)

    st.markdown("### Aktuelles Spiel:")

    current_players_string = ""
    for ingame_player in current_players:
        current_players_string+= f"""{ingame_player} - """
    current_players_string = current_players_string.rstrip(" -")
    st.metric("Mitspieler", current_players_string)
    col5, col6, col7 = st.columns([0.3, 0.3, 1])
    col5.metric("Spiel-count", game_number)
    col6.metric("Letzter Gewinner", last_winner)
    col7.metric("Letzter Verlierer", last_looser)
    col3, col4 = st.columns([0.3, 1])


    winner = col3.selectbox("Gewinner", current_players, index=0)
    looser = col4.selectbox("Verlierer", current_players, index=1)
    save_btn = st.button("Speichern")
    if save_btn:
        d_c.insert_new_game_results(session_id, winner=winner, looser=looser)
        d_c.update_player_scores(current_players, winner, looser)
        st.success("Gespeichert")

new_session_exp = st.expander("Neue Session")
player_names = list(d_c.return_players_table().names)
player_in_game = new_session_exp.multiselect("Mitspieler auswählen", player_names)

if len(player_in_game) > 0:
    iter_nr = 1
    new_session_exp.markdown("#### Reihenfolge:")
    for player in player_in_game:
        new_session_exp.write(f"Spieler {iter_nr}: {player}")
        iter_nr += 1

start_session_btn = new_session_exp.button("Starten")
col1, col2 = st.columns([0.3, 1])
end_session_btn = col1.button("Session beenden")
get_data_btn = col2.button("Sessions anzeigen")
refresh_btn = st.button("Aktualisieren")


if start_session_btn:
    if not is_open:
        session_id = d_c.start_new_session(player_in_game)
        d_c.create_session_table(session_id)
        new_session_exp.success(f"Neue Session gestartet")
        is_open, session_id, start_time, current_players = d_c.check_session_open()
    else:
        st.success(f"Session Nr. {session_id} noch offen. Beginn der Session: {d_p.unixtime_to_dt64(start_time)}")

if end_session_btn:
    if is_open:
        d_c.end_session(session_id)
        st.success("Session beendet")
        is_open, session_id, start_time, current_players = d_c.check_session_open()
    else:
        st.success("Keine Session offen")

if get_data_btn:
    st.table(d_c.return_sessions_table())

