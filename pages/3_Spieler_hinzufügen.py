import streamlit as st
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
.player-stats-font {
    font-size:32px;
    color: #75FB4C;
    text-align: center;
}
</style>""", unsafe_allow_html=True)

# Set base URL for API
BASE_URL = "https://avataaars.io/"

accessories_type_options = [
    "Blank",
    "Kurt",
    "Prescription01",
    "Prescription02",
    "Round",
    "Sunglasses",
    "Wayfarers",
]


top_type_options = [
    "NoHair",
    "Eyepatch",
    "Hat",
    "Hijab",
    "Turban",
    "WinterHat1",
    "WinterHat2",
    "WinterHat3",
    "WinterHat4",
    "LongHairBigHair",
    "LongHairBob",
    "LongHairBun",
    "LongHairCurly",
    "LongHairCurvy",
    "LongHairDreads",
    "LongHairFrida",
    "LongHairFro",
    "LongHairFroBand",
    "LongHairNotTooLong",
    "LongHairShavedSides",
    "LongHairMiaWallace",
    "LongHairStraight",
    "LongHairStraight2",
    "LongHairStraightStrand",
    "ShortHairDreads01",
    "ShortHairDreads02",
    "ShortHairFrizzle",
    "ShortHairShaggy",
    "ShortHairShaggyMullet",
    "ShortHairShortCurly",
    "ShortHairShortFlat",
    "ShortHairShortRound",
    "ShortHairShortWaved",
    "ShortHairSides",
    "ShortHairTheCaesar",
    "ShortHairTheCaesarSidePart",
]

# Create the Streamlit slider using the top_type_options list

hair_color_options = [
    "Auburn",
    "Black",
    "Blonde",
    "BlondeGolden",
    "Brown",
    "BrownDark",
    "PastelPink",
    "Platinum",
    "Red",
    "SilverGray",
]

# Create the Streamlit selectbox using the hair_color_options list


clothe_type_options = [
    "BlazerShirt",
    "BlazerSweater",
    "CollarSweater",
    "GraphicShirt",
    "Hoodie",
    "Overall",
    "ShirtCrewNeck",
    "ShirtScoopNeck",
    "ShirtVNeck",
]



eyebrow_type_options = [
    "Angry",
    "AngryNatural",
    "Default",
    "DefaultNatural",
    "FlatNatural",
    "RaisedExcited",
    "RaisedExcitedNatural",
    "SadConcerned",
    "SadConcernedNatural",
    "UnibrowNatural",
    "UpDown",
    "UpDownNatural",
]


eye_type_options = [
    "Close",
    "Default",
    "Dizzy",
    "EyeRoll",
    "Happy",
    "Hearts",
    "Side",
    "Squint",
    "Surprised",
    "Wink",
    "WinkWacky",
]


facial_hair_color_options = [
    "Auburn",
    "Black",
    "Blonde",
    "BlondeGolden",
    "Brown",
    "BrownDark",
    "Platinum",
    "Red",
]


facial_hair_type_options = [
    "Blank",
    "BeardMedium",
    "BeardLight",
    "BeardMagestic",
    "MoustacheFancy",
    "MoustacheMagnum",
]


hat_color_options = [
    "Black",
    "Blue01",
    "Blue02",
    "Blue03",
    "Gray01",
    "Gray02",
    "Heather",
    "PastelBlue",
    "PastelGreen",
    "PastelOrange",
    "PastelRed",
    "PastelYellow",
    "Pink",
    "Red",
    "White",
]



mouth_type_options = [
    "Concerned",
    "Default",
    "Disbelief",
    "Eating",
    "Grimace",
    "Sad",
    "ScreamOpen",
    "Serious",
    "Smile",
    "Tongue",
    "Twinkle",
    "Vomit",
]



skin_color_options = [
    "Tanned",
    "Yellow",
    "Pale",
    "Light",
    "Brown",
    "DarkBrown",
    "Black",
]


clothe_color_options = [
    "Black",
    "Blue01",
    "Blue02",
    "Blue03",
    "Gray01",
    "Gray02",
    "Heather",
    "PastelBlue",
    "PastelGreen",
    "PastelOrange",
    "PastelRed",
    "PastelYellow",
    "Pink",
    "Red",
    "White",
]


st.title("Spieler hinzufügen")
new_name = st.text_input("Name", key="player_name_input")
_,img_col, _ = st.columns(3)
avatar_img_placeholder = img_col.empty()
col1, col2, col3 = st.columns(3)

selected_facial_hair_type = col1.selectbox("Gesichtsbehaarung", facial_hair_type_options)
selected_facial_hair_color = col1.selectbox("Farbe Gesichtsbehaarung", facial_hair_color_options)
selected_hair_color = col1.selectbox("Haarfarbe:", hair_color_options)
selected_eyebrow_type = col1.selectbox("Augenbrauen", eyebrow_type_options)
selected_mouth_type = col2.selectbox("Mund", mouth_type_options)
selected_eye_type = col2.selectbox("Augen", eye_type_options)

selected_skin_color = col2.selectbox("Hautfarbe", skin_color_options)
selected_accessories_type = col2.selectbox("Accessoires", accessories_type_options)
selected_top_type = col3.selectbox("Kopfbedeckung", top_type_options)

if selected_top_type in [
    "Hat",
    "Hijab",
    "Turban",
    "WinterHat1",
    "WinterHat2",
    "WinterHat3",
    "WinterHat4"]:
    selected_hat_color = col3.selectbox("Farbe Kopfbedeckung", hat_color_options)
else:
    selected_hat_color = "Black"

selected_clothe_type = col3.selectbox("Kleidung", clothe_type_options)
selected_clothe_color = col3.selectbox("Farbe Kleidung", clothe_color_options)

avatar_url = f"{BASE_URL}?avatarStyle=Transparent&topType={selected_top_type}&accessoriesType={selected_accessories_type}&hairColor={selected_hair_color}&hatColor={selected_hat_color}&facialHairType={selected_facial_hair_type}&facialHairColor={selected_facial_hair_color}&clotheType={selected_clothe_type}&clotheColor={selected_clothe_color}&eyeType={selected_eye_type}&eyebrowType={selected_eyebrow_type}&mouthType={selected_mouth_type}&skinColor={selected_skin_color}"

avatar_img_placeholder.image(avatar_url)

def contains_only_letters(string):
    for character in string:
        if not character.isalpha():
            return False
    return True

add_player_btn = st.button("Hinzufügen")
if add_player_btn:
    if new_name and avatar_url and contains_only_letters(new_name):
        d_c.add_player(new_name, avatar_url)
        st.success("Spieler hinzugefügt")
    elif not new_name:
        st.error("Geben Sie einen Namen ein.")
    elif not avatar_url:
        st.error("Geben Sie den Link zu ihrem Avatar ein.")
    elif not contains_only_letters(new_name):
        st.error("Der Name darf nur Buchstaben enthalten.")
    else:
        st.error("Geben Sie den Namen und den Link zu ihrem Avatar ein.")
