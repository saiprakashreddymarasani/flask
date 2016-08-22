import sqlite3

# creating a new database
with sqlite3.connect('users.db') as connection:

    c = connection.cursor()

    c.execute('CREATE TABLE posts(username TEXT)')

    # insert dummy data into the table
    c.execute('INSERT INTO posts VALUES("sai")')
    c.execute('INSERT INTO posts VALUES("daniel")')

