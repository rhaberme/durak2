import streamlit as st
import database_connection as d_c
import pandas as pd
import altair as alt
import plotly.express as px
import graphviz

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

st.title("Statistik")

stats_df = d_c.return_players_table()
last_session_id = d_c.get_last_session_id()
game_number, last_winner, last_looser = d_c.return_last_game_results(last_session_id)

section_names_list = ["Gesamt", "Sessions", "Spieler"]
player_list = list(stats_df["names"])

selected_section = st.selectbox("", section_names_list)

if selected_section == "Sessions":
    session_table = d_c.return_sessions_table()
    sessions_ids_list = list(session_table.index)
    selected_session_id = st.selectbox("Session IDs", sessions_ids_list)
    if len(session_table) > 0:
        player_string = session_table.loc[selected_session_id].Fellow_Players
        player_string = player_string.lstrip("[")
        player_string = player_string.rstrip("]")
        player_string = player_string.replace("'", "")
        player_list = player_string.split(",")
        dot = graphviz.Digraph()
        dot.attr(rankdir='LR', size='10', bgcolor='#0F1116')
        dot.attr('node', shape='circle', style='filled', color='white', fixedsize='true', width='1')
        dot.attr('edge', color='white')

        last_player = None
        for player in player_list:
            if last_player:
                dot.edge(last_player, player)
                last_player = player
            else:
                last_player = player
        dot.edge(player_list[-1], player_list[0])

        st.graphviz_chart(dot)
        results_df = d_c.return_all_game_results_in_session(selected_session_id)
        results_df.rename(columns={"game_number": "Spiel", "winner": "Gewinner", "looser": "Verlierer",
                                        "game_time": "Dauer"}, inplace=True)
        results_df = results_df.set_index("Spiel")
        # results_df['Dauer'] = results_df['Dauer'].apply(lambda x: x/3600)

        st.table(results_df)


elif selected_section == "Spieler":
    players_list = d_c.return_players_table().names
    player_selected = st.selectbox("Wählen:", players_list)
    sessions_table = d_c.return_sessions_table()
    played_sessions = [x[0] for x in sessions_table.iterrows() if player_selected in x[1].Fellow_Players]
    game_number = 0
    results_list = []
    win_number = 0
    wins = []
    loss_number = 0
    losses = []

    for session_id in played_sessions:
        results_df = d_c.return_all_game_results_in_session(session_id)
        for row in results_df.iterrows():
            game_number += 1
            if row[1].winner == player_selected:
                results_list.append(1)
                win_number += 1
                wins.append(win_number)
                losses.append(loss_number)
            elif row[1].looser == player_selected:
                results_list.append(-1)
                loss_number += 1
                wins.append(win_number)
                losses.append(loss_number)
            else:
                results_list.append(0)
                wins.append(win_number)
                losses.append(loss_number)

    game_numbers = list(range(0, game_number))
    player_stats_df = pd.DataFrame({'Spiele': game_numbers, 'Ergebnis': results_list})
    wins_losses_df = pd.DataFrame({"x": game_numbers, "wins": wins, "losses": losses})

    fig = px.line(wins_losses_df, x='x', y='wins', labels={'wins': 'Wins'}, template="plotly_dark",
                  )
    fig.add_bar(x=wins_losses_df['x'], y=wins_losses_df['losses'], name='Losses')
    fig.update_layout(xaxis_title="Spiele",
                      yaxis_title="WINS / LOSSES",
                      showlegend=False,
                      xaxis_showgrid=False,
                      yaxis_showgrid=False,
                      plot_bgcolor='rgba(0,0,0,0)')

    st.plotly_chart(fig, use_container_width=True)

    chart = alt.Chart(player_stats_df).mark_bar().encode(
        x='Spiele:O',  # x-axis is ordinal
        y='Ergebnis:Q',  # y-axis is quantitative
        color=alt.Color('Ergebnis:Q', scale=alt.Scale(range=['red', 'green']))  # color negative values red
    )
    st.altair_chart(chart, use_container_width=True)

else:
    best_ratio = 0
    best_player = ""
    for row in stats_df.iterrows():
        new_ratio = row[1].games/row[1].losses
        if new_ratio > best_ratio:
            best_ratio = new_ratio
            best_player = row[1].names

    for player in player_list:
        col0, col1, col2, col3, col4, col5, col6, col7 = st.columns([0.8, 1.8, 1, 1, 1, 1,1 ,1])
        st.write(" ")
        if player == best_player:
            col0.image("pics/gold_medal.png", width=50)
        col1.metric("", player)
        col2.metric("Spiele", stats_df[stats_df["names"]==player]["games"])
        if player == last_winner:
            col3.metric("Gewonnen", stats_df[stats_df["names"]==player]["wins"], delta=1)

            try:
                old_loss_games_quota = round(
                     (int(stats_df[stats_df["names"] == player]["games"])-1) /
                     (int(stats_df[stats_df["names"] == player]["losses"]))
                    , 2)
            except ZeroDivisionError:
                old_loss_games_quota = 0

            try:
                old_win_loss_quota = round(
                    (int(stats_df[stats_df["names"] == player]["wins"]) -1) / (int(stats_df[stats_df["names"] == player]["losses"])), 2)
            except ZeroDivisionError:
                old_win_loss_quota = 0

            try:
                old_win_games_quota = round(
                    (int(stats_df[stats_df["names"] == player]["wins"]) -1) / (int(stats_df[stats_df["names"] == player]["games"])-1), 2)
            except ZeroDivisionError:
                old_win_games_quota = 0
        else:
            col3.metric("Gewonnen", stats_df[stats_df["names"]==player]["wins"])

        if player == last_looser:
            col4.metric("Verloren", stats_df[stats_df["names"]==player]["losses"], delta=-1)

            try:
                old_loss_games_quota = round(
                     (int(stats_df[stats_df["names"] == player]["games"])-1) /
                    (int(stats_df[stats_df["names"] == player]["losses"])-1), 2)
            except ZeroDivisionError:
                old_loss_games_quota = 0

            try:
                old_win_loss_quota = round(
                    (int(stats_df[stats_df["names"] == player]["wins"])) / (int(stats_df[stats_df["names"] == player]["losses"])-1), 2)
            except ZeroDivisionError:
                old_win_loss_quota = 0

            try:
                old_win_games_quota = round(
                    int(stats_df[stats_df["names"] == player]["wins"]) / (int(stats_df[stats_df["names"] == player]["games"])-1), 2)
            except ZeroDivisionError:
                old_win_games_quota = 0
        else:
            col4.metric("Verloren", stats_df[stats_df["names"]==player]["losses"])

        try:
            win_loss_quota = round(
                int(stats_df[stats_df["names"] == player]["wins"]) / int(stats_df[stats_df["names"] == player]["losses"]), 2)
        except ZeroDivisionError:
            win_loss_quota = "TBD"

        try:
            win_games_quota = round(
                int(stats_df[stats_df["names"] == player]["wins"]) / int(stats_df[stats_df["names"] == player]["games"]), 2)
        except ZeroDivisionError:
            win_games_quota = "TBD"

        try:
            loss_games_quota = round(
                int(stats_df[stats_df["names"] == player]["games"])/
                int(stats_df[stats_df["names"] == player]["losses"]), 2)
        except ZeroDivisionError:
            loss_games_quota = "TBD"


        if (player != last_winner and player != last_looser) or win_loss_quota == "TBD" or win_loss_quota==0.0:
            col5.metric("WIN/LOSS", win_loss_quota)
        else:
            col5.metric("WIN/LOSS", win_loss_quota, delta=round(win_loss_quota - old_win_loss_quota, 2))

        if (player != last_winner and player != last_looser) or win_games_quota == "TBD" or win_games_quota==0.0:
            col6.metric("WIN/GAMES", win_games_quota)
        else:
            col6.metric("WIN/GAMES", win_games_quota, delta=round(win_games_quota - old_win_games_quota, 2))

        if (player != last_winner and player != last_looser) or loss_games_quota == "TBD" or loss_games_quota==0.0:
            col7.metric("GAMES/LOSSES", loss_games_quota)
        else:
            col7.metric("GAMES/LOSSES", loss_games_quota, delta=round(loss_games_quota - old_loss_games_quota, 2))

