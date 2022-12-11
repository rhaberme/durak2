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


st.table(d_c.return_players_table())