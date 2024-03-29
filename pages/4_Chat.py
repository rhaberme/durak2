import streamlit as st
import datetime
import database_connection as d_c
import yaml
import hashlib

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


password_file = yaml.safe_load(open(r"database/settings.yml"))
passwords = password_file['passwords']

if "logged_in" not in st.session_state.keys() or not st.session_state["logged_in"]:
    with st.form(key='my_form'):
        username = st.text_input('Benutzername')
        password = st.text_input('Passwort', type="password")
        login_submit_button = st.form_submit_button('Login')
        if login_submit_button:
            password_hash = hashlib.sha224(password.encode()).hexdigest()
            if passwords[username] == password_hash:
                st.session_state["username"] = username
                st.session_state["password"] = password
                st.session_state["logged_in"] = True
                st.experimental_rerun()
            else:
                st.error("Benutzername und Passwort ist falsch.")

if "logged_in" in st.session_state.keys() and st.session_state["logged_in"]:
    message_placeholder = st.empty()
    text_input_placeholder = st.empty()

    message = text_input_placeholder.text_input('Nachricht:', '')


    if st.button("Senden"):
        now = datetime.datetime.now()
        time_string = now.strftime('%Y-%m-%d %H:%M:%S')
        d_c.insert_message(time_string, message)

    col1, col2 = message_placeholder.columns([0.2, 0.6])
    messages_list = d_c.return_table("Messages", "database/messages_db.db")
    for message in messages_list:
        col1.write(message[0])
        if message[1] != "":
            col2.write(message[1])
        else:
            col2.write("o")


