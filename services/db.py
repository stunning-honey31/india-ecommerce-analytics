import sqlite3

def get_connection():
    return sqlite3.connect("db/shop.db", check_same_thread=False)
