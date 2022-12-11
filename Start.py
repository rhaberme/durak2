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
.big-font-green {
    font-size:32px;
    color: green;
}
</style>""", unsafe_allow_html=True)

st.title("Sessions")


@st.experimental_singleton
def init_connection():
    return sqlite3.connect("database/durak_db")

st.markdown("### Aktuelles Spiel:")

winner_looser_placeholder = st.empty()
save_btn_placeholder = st.empty()
player_ingame_placeholder= st.empty()
col5, col6, col7 = st.columns(3)

is_open, session_id, start_time, player_ingame = d_c.check_session_open()

if is_open:
    current_players = d_c.return_sessions_table().loc[session_id].Fellow_Players
    current_players = current_players.replace("[", "")
    current_players = current_players.replace("]", "")
    current_players = current_players.replace(" ", "")
    current_players = current_players.replace("'", "")

    current_players = current_players.split(",")

    game_number, last_winner, last_looser = d_c.return_last_game_results(session_id)


    current_players_string = ""
    for ingame_player in current_players:
        current_players_string+= f"""{ingame_player} - """
    current_players_string = current_players_string.rstrip(" -")


    player_ingame_placeholder.markdown("Mitspieler: "+ f'<p class="big-font-green">{current_players_string}</p>', unsafe_allow_html=True)

    col5.metric("Spiel-count", game_number)
    col6.metric("Letzter Gewinner", last_winner)
    col7.metric("Letzter Verlierer", last_looser)

    col3, col4 = winner_looser_placeholder.columns(2)
    winner = col3.selectbox("Gewinner", ["-"] + current_players, index=0)
    looser = col4.selectbox("Verlierer", ["-"] + current_players, index=0)
    save_btn = save_btn_placeholder.button("Speichern")
    if save_btn:
        if (winner != "-" and looser != "-") and winner != looser:
            d_c.insert_new_game_results(session_id, winner=winner, looser=looser)
            d_c.update_player_scores(current_players, winner, looser)
            st.success("Gespeichert")
            st.experimental_rerun()
        elif winner == "-":
            st.error("Kein Gewinner ausgewählt")
        elif looser == "-":
            st.error("Kein Verlierer ausgewählt")
        else:
            st.error(f"{winner} kann nicht gleichzeitig gewonnen und verloren haben.")


    end_session_btn = st.button("Session beenden")

    if end_session_btn:
        if is_open:
            d_c.end_session(session_id)
            st.success("Session beendet")
            is_open, session_id, start_time, current_players = d_c.check_session_open()
            st.experimental_rerun()

        else:
            st.success("Keine Session offen")
else:

    # new_session_exp = st.expander("Neue Session")
    player_names = list(d_c.return_players_table().names)
    player_in_game = st.multiselect("Mitspieler auswählen", player_names)

    if len(player_in_game) > 0:
        iter_nr = 1
        st.markdown("#### Reihenfolge:")
        for player in player_in_game:
            st.write(f"Spieler {iter_nr}: {player}")
            iter_nr += 1

    start_session_btn = st.button("Starten")
    if start_session_btn:
        if not is_open:
            session_id = d_c.start_new_session(player_in_game)
            d_c.create_session_table(session_id)
            st.success(f"Neue Session gestartet")
            is_open, session_id, start_time, current_players = d_c.check_session_open()
            st.experimental_rerun()

        else:
            st.success(f"Session Nr. {session_id} noch offen. Beginn der Session: {d_p.unixtime_to_dt64(start_time)}")

#get_data_btn = st.button("Sessions anzeigen")

#if get_data_btn:
#    st.table(d_c.return_sessions_table())

