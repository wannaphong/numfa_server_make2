# -*- coding: utf-8 -*-
import sqlite3
db_file="db_chatlog.db"
def create_connection():
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
def setup():
	try:
		create_connection()
		conn = sqlite3.connect(db_file)
		create_table_sql="CREATE TABLE IF NOT EXISTS chatlog (id integer PRIMARY KEY,txtget text NOT NULL,txtsent text NOT NULL,sqltime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)"
		create_table(conn,create_table_sql)
		print("setup ok")
		conn.close()
	except Error as e:
		print(e)
def add_data(textget,textsent):
	conn = sqlite3.connect(db_file)
	sql = "INSERT INTO chatlog (txtget,txtsent) VALUES (?,?)"
	cur = conn.cursor()
	cur.execute(sql, (str(textget),str(textsent)))
	conn.commit()
	#print(True)
	conn.close()