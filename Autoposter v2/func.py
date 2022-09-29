import configparser
from pyrogram import Client, filters
import re
import sqlite3
def get_api(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    api_id = config["Telegram"]["api_id"]
    api_hash = config["Telegram"]["api_hash"]
    username = config["Telegram"]["username"]
    api = {
    "api_id" : api_id,
    "api_hash" : api_hash,
    "username" : username
    }
    return api

def Insert_msg(id, input, output):
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO msg(msg_id, input, output) VALUES(?, ?, ?)''', (id, input, output))

def Insert_group_msg(id, group_id, input, output):
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO group_msg(msg_id, group_id, input, output) VALUES(?, ?, ?, ?)''', (id, group_id, input, output))

def Get_messages_id(input, output):
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        ids = cursor.execute('''SELECT msg_id FROM msg WHERE input = ? AND output = ?''', (input, output)).fetchall()
        ids = [int(x[0]) for x in ids]
        return ids

def Get_group_messages_id(input, output):
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        ids = cursor.execute('''SELECT msg_id FROM group_msg WHERE input = ? AND output = ?''', (input, output)).fetchall()
        ids = [int(x[0]) for x in ids]
        return ids

def Get_media_group_id(input, output):
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        ids = cursor.execute('''SELECT group_id FROM group_msg WHERE input = ? AND output = ?''', (input, output)).fetchall()
        ids = [int(x[0]) for x in ids]
        return ids

def Delete_msg_id(id, inp, out):
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        ids = cursor.execute('''DELETE FROM msg WHERE msg_id = ? AND input = ? AND output = ?''', (id, inp, out))
def Delete_group_id(id, inp, out):
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        ids = cursor.execute('''DELETE FROM group_msg WHERE msg_id = ? AND input = ? AND output = ?''', (id, inp, out))

def Get_channels():
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        channels_step = cursor.execute('''SELECT input, output, mode FROM channels''').fetchall()
        channels = []
        # print(channels_step[0])
        for x, y, z in channels_step:
            # x = int(x)
            # y = int(y)
            # z = str(z)

            channels.append((int(x), int(y), str(z)))
        return channels

def filter2(text):
    # link = re.search(r'http', text)
    # if link:
    #     return True
    # return False
    return True

def add_channel(inp, out):
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO channels(input, output) VALUES(?, ?)''', (inp, out))

def drop_all():
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''DROP TABLE IF EXISTS msg ''')
        cursor.execute('''DROP TABLE IF EXISTS group_msg ''')
        cursor.execute('''DROP TABLE IF EXISTS channels ''')

def Delete_msg():
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM msg''')
        cursor.execute('''DELETE FROM group_msg''')
def Delete_channels():
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM channels''')
def Delete_all():
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM channels''')
        cursor.execute('''DELETE FROM group_msg''')
        cursor.execute('''DELETE FROM msg''')

def Drop_table(table_name):
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f'''DROP TABLE {table_name}''')
def create_bd():
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS msg(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        msg_id TEXT,
        input TEXT,
        output TEXT
        );''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS group_msg(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        msg_id TEXT,
        group_id INTEGER UNIQUE,
        input TEXT,
        output TEXT
        );''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS channels(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input TEXT,
        output TEXT,
        mode TEXT
        );''')
