import sqlite3


connection = sqlite3.connect('database.db', check_same_thread=False)

with open('schema.sql') as f:
    connection.executescript(f.read())
db = connection.cursor()
