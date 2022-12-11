import streamlit as st

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
st.title("Statistik")

stats_df = d_c.return_players_table()
last_session_id = d_c.get_last_session_id()
game_number, last_winner, last_looser = d_c.return_last_game_results(last_session_id)

section_names_list = ["Gesamt", "Sessions", "Spieler"]
player_list = list(stats_df["names"])


selected_section = st.selectbox("", section_names_list)

if selected_section == "Sessions":
    pass

elif selected_section == "Spieler":
    pass

else:
    # st.table(stats_df)


    for player in player_list:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("", player)
        col2.metric("Spiele", stats_df[stats_df["names"]==player]["games"])
        if player == last_winner:
            col3.metric("Gewonnen", stats_df[stats_df["names"]==player]["wins"], delta=1)
        else:
            col3.metric("Gewonnen", stats_df[stats_df["names"]==player]["wins"])

        if player == last_looser:
            col4.metric("Verloren", stats_df[stats_df["names"]==player]["losses"], delta=-1)
        else:
            col4.metric("Verloren", stats_df[stats_df["names"]==player]["losses"])


