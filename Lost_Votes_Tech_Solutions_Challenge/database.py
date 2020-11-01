# DB Management
# DB Functions

# Database Creation & Connection
import sqlite3
from sqlite3 import Connection
import streamlit as st
URI_SQLITE_DB = "Voters.db"

"""
check_same_thread = False is added to avoid same thread issue
"""
conn = sqlite3.connect(URI_SQLITE_DB, check_same_thread=False)
c = conn.cursor()

@st.cache(hash_funcs={Connection: id})
def get_connection(path: str):
    """Put the connection in cache to reuse if path does not change between Streamlit reruns.
    NB : https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
    """
    return sqlite3.connect(path, check_same_thread=False)

def create_usertable(conn: Connection):
  c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT PRIMARY KEY,password TEXT)')

def add_userdata(conn: Connection,username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(conn: Connection,username,password):
  c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
  data = c.fetchall()
  return data

def view_all_users(conn: Connection):
  c.execute('SELECT * FROM userstable')
  data = c.fetchall()
  return data

def create_table(conn: Connection):
	c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,article TEXT,postdate DATE)')

def add_data(conn: Connection,author, title, article, postdate):
	c.execute('INSERT INTO blogtable(author,title,article,postdate) VALUES (?,?,?,?)',(author,title,article,postdate))
	conn.commit()

def view_all_posts(conn: Connection):
	c.execute('SELECT * FROM blogtable')
	data = c.fetchall()
	return data

def view_all_titles(conn: Connection):
	c.execute('SELECT DISTINCT title FROM blogtable')
	data = c.fetchall()
	return data

def get_blog_by_title(conn: Connection,title):
	c.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
	data = c.fetchall()
	return data

def get_blog_by_author(conn: Connection,author):
	c.execute('SELECT * FROM blogtable WHERE author="{}"'.format(author))
	data = c.fetchall()
	return data

def delete_data(conn: Connection,title):
	c.execute('DELETE FROM blogtable WHERE title="{}"'.format(title))
	conn.commit()