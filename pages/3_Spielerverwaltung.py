import streamlit as st

import data_processing as d_p
import database_connection as d_c

st.set_page_config(
    page_title="Durak",
    page_icon="🃏",
)

# hide_menu = """
# <style>
# #MainMenu {visibility:hidden;}
# footer{visibility:hidden;}
# </style>
# """
# st.markdown(hide_menu, unsafe_allow_html=True)

st.title("Spielerverwaltung")

st.markdown("## Spieler hinzufügen")

st.markdown("### 1. Name wählen:")
new_name = st.text_input("Name", key="player_name_input")
st.markdown("### 2. Avatar erstellen:")
st.write("[Link](https://getavataaars.com/?accessoriesType=Round&avatarStyle=Transparent&clotheColor=Gray01&clotheType=GraphicShirt&eyeType=Hearts&eyebrowType=DefaultNatural&facialHairColor=Brown&facialHairType=Blank&graphicType=SkullOutline&hairColor=Platinum&hatColor=Red&mouthType=Disbelief&skinColor=Brown&topType=WinterHat4)")
st.markdown("### 3. Link zu Avatar einfügen:")
avatar_link = st.text_input("Avatar-Link", key="avatar_link_input")

add_player_btn = st.button("Hinzufügen")
if add_player_btn:
    if new_name and avatar_link:
        d_c.add_player(new_name, avatar_link)
        st.success("Spieler hinzugefügt")
    elif not new_name:
        st.error("Geben Sie einen Namen ein.")
    elif not avatar_link:
        st.error("Geben Sie den Link zu ihrem Avatar ein.")
    else:
        st.error("Geben Sie den Namen und den Link zu ihrem Avatar ein.")

# st.markdown("## Spieler entfernen")
# player_names = list(d_c.return_players_table().names)
# selected_player = st.selectbox("Spieler wählen", player_names)
# remove_player_btn = st.button("Entfernen")

# if remove_player_btn:
#    d_c.remove_player(selected_player)