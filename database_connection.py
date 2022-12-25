import sqlite3
import pandas as pd
import time

import data_processing as d_p

def return_table(table_name, database):
    con = sqlite3.connect(database)
    cursor = con.cursor()
    try:
        cursor.execute(f"""SELECT * FROM '{table_name}'""")
    except sqlite3.OperationalError:
        create_session_table(table_name)
        cursor.execute(f"""SELECT * FROM '{table_name}'""")

    return cursor.fetchall()

def return_sessions_table():
    rows = return_table(table_name="Sessions", database="database/durak_db")
    dt64_rows = []
    for row in rows:
        if row[2] == 0:
            dt64_rows.append((row[0], d_p.unixtime_to_dt64(row[1]), None, row[3]))
        else:
            dt64_rows.append((row[0], d_p.unixtime_to_dt64(row[1]), d_p.unixtime_to_dt64(row[2]), row[3]))
    rows_df = pd.DataFrame(dt64_rows, columns=["Session_id", "Start_Time", "End_Time", "Fellow_Players"])
    rows_df = rows_df.set_index("Session_id")

    return rows_df


def check_session_open():
    try:
        con = sqlite3.connect("database/durak_db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Sessions")
        rows_df = pd.DataFrame(cursor.fetchall(), columns=["Session_id", "Start_Time", "End_Time", "Fellow_Players"])
        rows_df = rows_df.set_index("Session_id")
        max_session_id = rows_df.index.max()
        cursor.close()
        if len(rows_df) == 0:
            return False, 0, 0, ""
        if rows_df.loc[max_session_id]["End_Time"] == 0:
            return True, max_session_id, rows_df.loc[max_session_id]["Start_Time"], rows_df.loc[max_session_id]["Fellow_Players"]
        else:
            return False, max_session_id, rows_df.loc[max_session_id]["Start_Time"], rows_df.loc[max_session_id]["Fellow_Players"]

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if con:
            con.close()
            print("The SQLite connection is closed")


def get_last_session_id():
        con = sqlite3.connect("database/durak_db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Sessions")
        rows_df = pd.DataFrame(cursor.fetchall(),
                               columns=["Session_id", "Start_Time", "End_Time", "Fellow_Players"])
        rows_df = rows_df.set_index("Session_id")
        cursor.close()
        if con:
            con.close()
        return rows_df.index.max()


def end_session(session_id):
    try:
        con = sqlite3.connect("database/durak_db")
        cursor = con.cursor()
        sql = f''' UPDATE Sessions
              SET End_Time = {round(time.time())}
              WHERE Session_ID = {session_id}'''
        cursor.execute(sql)
        con.commit()
    except sqlite3.Error as error:
        print("Failed to write data to sqlite table", error)
    finally:
        if con:
            con.close()
            print("The SQLite connection is closed")

def start_new_session(fellow_players):
    try:
        con = sqlite3.connect("database/durak_db")
        cursor = con.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute("SELECT * FROM Sessions")
        rows_df = pd.DataFrame(cursor.fetchall(), columns=["Session_id", "Start_Time", "End_Time", "Fellow_Players"])
        rows_df = rows_df.set_index("Session_id")
        session_id = 1 if len(rows_df) == 0 else rows_df.index.max() + 1
        sqlite_insert_query = f"""INSERT INTO Sessions
                              (session_id, Start_Time, End_Time, Fellow_Players) 
                               VALUES 
                              ({session_id}, {round(time.time())}, {0}, "{fellow_players}")"""
        count = cursor.execute(sqlite_insert_query)
        con.commit()
        print("Record inserted successfully into Sessions table ", cursor.rowcount)
        cursor.close()


    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if con:
            con.close()
            print("The SQLite connection is closed")
        return session_id


def return_players_table():
    con = sqlite3.connect("database/durak_db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Players")

    rows = cursor.fetchall()
    rows_df = pd.DataFrame(rows, columns=["player_ids", "names", "games", "wins", "losses"])
    rows_df = rows_df.set_index("player_ids")

    return rows_df


def return_players_avatar_link(player_name):
    con = sqlite3.connect("database/durak_db")
    cursor = con.cursor()
    cursor.execute(f"""SELECT avatar_link FROM Avatar_Links
                   WHERE player_name = "{player_name}"
                   """)

    avatar_link = cursor.fetchall()[0][0]
    return avatar_link

def add_player(new_name, avatar_link):
    try:
        # todo: check if player_name and avatar_link is unique
        con = sqlite3.connect("database/durak_db")
        cursor = con.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute("SELECT * FROM Players")
        rows_df = pd.DataFrame(cursor.fetchall(), columns=["player_id", "player_name", "games", "wins", "losses"])
        rows_df = rows_df.set_index("player_id")
        player_id = 1 if len(rows_df) == 0 else rows_df.index.max() + 1
        sqlite_insert_query = f"""INSERT INTO Players
                               (player_id, player_name, games, wins, losses) 
                              VALUES 
                              ({player_id}, "{new_name}", 0, 0, 0)"""

        count = cursor.execute(sqlite_insert_query)
        print("Record inserted successfully into Players table ", cursor.rowcount)

        con.commit()
        avatar_link = avatar_link.lstrip("<img src='")
        avatar_link = avatar_link.rstrip("' />")

        sqlite_insert_query2 = f"""INSERT INTO Avatar_Links
                               (player_id, player_name, avatar_link) 
                              VALUES 
                              ({player_id}, "{new_name}", "{avatar_link}")"""
        count = cursor.execute(sqlite_insert_query2)
        print("Record inserted successfully into Avatar_Link table ", cursor.rowcount)
        con.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if con:
            con.close()
            print("The SQLite connection is closed")


def remove_player(player_name):
    try:
        con = sqlite3.connect("database/durak_db")
        cursor = con.cursor()
        print("Successfully Connected to SQLite")
        sqlite_insert_query = f"""DELETE FROM Players
                               WHERE player_name = "{player_name}"
                               """

        count = cursor.execute(sqlite_insert_query)
        con.commit()
        print("Record deleted successfully from Players table ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete data from sqlite table", error)
    finally:
        if con:
            con.close()
            print("The SQLite connection is closed")



def do_sql(sql_command, database):
    try:
        con = sqlite3.connect(database)
        cursor = con.cursor()
        print("Successfully Connected to SQLite")

        count = cursor.execute(sql_command)
        con.commit()
        print("Command successful ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to do command", error)
    finally:
        if con:
            con.close()
            print("The SQLite connection is closed")


def create_session_table(session_id):
    session_id = str(session_id)
    sql_command = f"""CREATE TABLE '{session_id}' (
                    Game_Number int,
                    winner varchar(16),
                    looser varchar(16),
                    Game_Time int
                );"""
    print("!!")
    do_sql(sql_command,"database/session_db")



def insert_new_game_results(session_id, winner, looser):
    game_result_table = return_table(session_id, "database/session_db")
    if len(game_result_table) == 0:
        max_game_number = 1
    else:
        print(pd.DataFrame(game_result_table))

        max_game_number = max(pd.DataFrame(game_result_table, columns=["game_number", "winner", "looser",
                                                                       "game_time"]).game_number)
        max_game_number += 1
    sql_command = f"""INSERT INTO "{session_id}"
                    VALUES ({max_game_number}, "{winner}", "{looser}", {round(time.time())});"""
    do_sql(sql_command, "database/session_db")
    print("Game was added")
    return max_game_number, winner, looser


def return_game_results(session_id):
    game_result_table_df = pd.DataFrame(return_table(session_id, "database/session_db"), columns=["game_number", "winner", "looser",
                                                                   "game_time"])
    if len(game_result_table_df)>0:
        max_game_number = max(game_result_table_df.game_number)
        winner = str(game_result_table_df[game_result_table_df["game_number"]==max_game_number].winner).split()[1]
        looser = str(game_result_table_df[game_result_table_df["game_number"]==max_game_number].looser).split()[1]

        return max_game_number, winner, looser
    else:
        return 0, "", ""


def update_player_scores(current_players, winner, looser):

    for player in current_players:
        if player == winner:
            sql = f''' UPDATE Players
                          SET games = games + 1, wins = wins + 1 
                          WHERE player_name = "{player}"'''

        elif player == looser:
            sql = f''' UPDATE Players
                          SET games = games + 1, losses = losses + 1 
                          WHERE player_name = "{player}"'''
        else:
            sql = f''' UPDATE Players
                          SET games = games + 1 
                          WHERE player_name = "{player}"'''

        do_sql(sql_command=sql, database="database/durak_db")