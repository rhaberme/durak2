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
st.title("Spielerverwaltung")

st.markdown("## Spieler hinzufügen")
new_name = st.text_input("Name:")
add_player_btn = st.button("Hinzufügen")
if add_player_btn:
    d_c.add_player(new_name)
    st.success("Spieler hinzugefügt")

st.markdown("## Spieler entfernen")
player_names = list(d_c.return_players_table().names)
selected_player = st.selectbox("Spieler wählen", player_names)
remove_player_btn = st.button("Entfernen")

if remove_player_btn:
    d_c.remove_player(selected_player)