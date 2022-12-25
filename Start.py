import streamlit as st
from st_clickable_images import clickable_images
import sqlite3

import database_connection as d_c
import data_processing as d_p

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
.player-ingame-font {
    font-size:32px;
    color: #75FB4C;
    text-align: center;
}
</style>""", unsafe_allow_html=True)

st.title("Sessions")


@st.experimental_singleton
def init_connection():
    return sqlite3.connect("database/durak_db")

first_placeholder_title = st.empty()
#winner_looser_placeholder = st.empty()
#save_btn_placeholder = st.empty()
#player_ingame_placeholder= st.empty()

is_open, session_id, start_time, player_ingame = d_c.check_session_open()

if is_open:
    first_placeholder_title.markdown("## Aktuelles Spiel:")

    current_players = d_c.return_sessions_table().loc[session_id].Fellow_Players
    current_players = current_players.replace("[", "")
    current_players = current_players.replace("]", "")
    current_players = current_players.replace(" ", "")
    current_players = current_players.replace("'", "")

    current_players = current_players.split(",")
    # https://getavataaars.com/?accessoriesType=Wayfarers&avatarStyle=Circle&clotheType=ShirtCrewNeck&eyeType=Cry&eyebrowType=RaisedExcitedNatural&facialHairType=MoustacheMagnum&hairColor=SilverGray&mouthType=Serious&skinColor=DarkBrown&topType=LongHairCurvy
    if "winner" not in st.session_state.keys():
        st.session_state["winner"] = None

    if "looser" not in st.session_state.keys():
        st.session_state["looser"] = None

    if "winner" in st.session_state.keys() and  st.session_state["winner"] != None:
        st.session_state["img_src_list"] = [d_c.return_players_avatar_link(x) for x in current_players]
        st.session_state["img_src_list"][st.session_state["winner"]] = d_p.change_avatar(
            st.session_state["img_src_list"][st.session_state["winner"]], win=True)
    else:
        st.session_state["img_src_list"] = [d_c.return_players_avatar_link(x) for x in current_players]
    if "looser" in st.session_state.keys() and st.session_state["looser"] != None:
        st.session_state["img_src_list"][st.session_state["looser"]] = d_p.change_avatar(st.session_state["img_src_list"][st.session_state["looser"]], win=False)

    clicked = clickable_images(
        st.session_state["img_src_list"],
        titles=[f"{current_players[i]}" for i in range(len(st.session_state["img_src_list"]))],
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "5px", "height": "100px"},
    )


    if clicked >= 0 and st.session_state["winner"] is None:
        st.session_state["winner"] = clicked
        st.experimental_rerun()

    elif clicked >=0 and st.session_state["looser"] is None:
        st.session_state["looser"] = clicked
        st.experimental_rerun()
    elif clicked >=0 and (st.session_state["winner"] is not None and st.session_state["looser"] is not None):
        st.session_state["winner"] = None
        st.session_state["looser"] = None
        st.experimental_rerun()

    if st.session_state["winner"] != None:
        st.markdown(f"#### Gewinner: {current_players[st.session_state['winner']]}")

    if st.session_state["looser"] != None:
        st.markdown(f"#### Verlierer: {current_players[st.session_state['looser']]}")

    # st.markdown(f"Spieler {current_players[clicked]} ausgewählt" if clicked > -1 else "No image clicked")

    game_number, last_winner, last_looser = d_c.return_game_results(session_id)


    current_players_string = ""
    for ingame_player in current_players:
        current_players_string+= f"""{ingame_player} &ensp;"""

    # player_ingame_placeholder.markdown('<section>Mitspieler:</section>'+ f'<section class="player-ingame-font">{current_players_string}</section>',
    #                                  unsafe_allow_html=True)


    save_btn = st.button("Speichern")
    if save_btn:
        winner = current_players[st.session_state["winner"]]
        looser = current_players[st.session_state["looser"]]
        if (winner != "-" and looser != "-") and winner != looser:
            d_c.insert_new_game_results(session_id, winner=winner, looser=looser)
            d_c.update_player_scores(current_players, winner, looser)
            st.success("Gespeichert")
            st.session_state["winner"] = None
            st.session_state["looser"] = None
            st.experimental_rerun()
        elif winner == "-":
            st.error("Kein Gewinner ausgewählt")
        elif looser == "-":
            st.error("Kein Verlierer ausgewählt")
        else:
            st.error(f"{winner} kann nicht gleichzeitig gewonnen und verloren haben.")


    st.markdown("## Letztes Spiel:")
    col5, col6, col7 = st.columns(3)

    col7.metric("Spiel-Nr.", game_number)
    if last_winner != "":
        col5.metric("", last_winner, delta="+ Sieg")
    if last_looser != "":
        col6.metric("", last_looser, delta="- Niederlage")



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
    first_placeholder_title.markdown("### Neues Spiel starten:")
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

        if len(player_in_game) > 1:
            session_id = d_c.start_new_session(player_in_game)
            d_c.create_session_table(session_id)
            st.success(f"Neue Session gestartet")
            is_open, session_id, start_time, current_players = d_c.check_session_open()
            st.experimental_rerun()

        else:
            st.error(f"Wählen Sie mindestens 2 Spieler aus.")

#get_data_btn = st.button("Sessions anzeigen")

#if get_data_btn:
#    st.table(d_c.return_sessions_table())

