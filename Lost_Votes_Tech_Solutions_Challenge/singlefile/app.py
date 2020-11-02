import streamlit as st
import pandas as pd
import base64
from PIL import Image

# DB Management
# DB Functions

# Database Creation & Connection
import sqlite3
from sqlite3 import Connection
import streamlit as st

# Security
#passlib,hashlib,bcrypt,scrypt

import hashlib

URI_SQLITE_DB = "Voters.db"

html_temp = """
    <body style="background-color:green;">
    <div style="background-color:green;padding:10px">
    <h2 style="color:white;text-align:center;">Lost Votes Tech Solutions Challenge</h2>
    </div>
    </body>
"""
st.set_page_config(
        page_title = 'Votes',
        page_icon = "✌",
        layout = "centered",
        initial_sidebar_state = "expanded"
    )

def make_hashes(password):
  return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
  if make_hashes(password) == hashed_text:
    return hashed_text
  return False
  
# """
# check_same_thread = False is added to avoid same thread issue
# """
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

def main():
	
    """Lost_Votes_Tech_Solutions_Challenge"""
    #st.title("Lost Votes Tech Solutions Challenge")
    st.markdown(html_temp, unsafe_allow_html=True)
    menu = ["Home","Login","SignUp","About"]
    st.markdown(
    """
	<style>
	.sidebar .sidebar-content {
	    background-image: linear-gradient(#264D59, #43978D, #F9E07F, #F9AD6A, #D46C4E);
	    color: blue;
	}
	</style>
	""",
	    unsafe_allow_html=True,
	)

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Problem Statement Brief:")
        st.write("All adults have a right to vote, but this right is not being exercised due to thelimitation of voting in the registered constituency by being physically there.")

        st.subheader("Proposed Solution:")
        img = Image.open("Solution.png")
        st.image(img, width=750, caption="Solution")

    elif choice == "Login":
      st.subheader("**Please Login to avail the vote!**")

      username = st.sidebar.text_input("Adhar/Passport/VoterID")
      password = st.sidebar.text_input("Password",type='password')
    
      if st.sidebar.checkbox("Login"):
        #create_usertable()
        hashed_pswd = make_hashes(password)
        result = login_user(conn,username,check_hashes(password,hashed_pswd))
        if result:
           st.success("Logged In as {}".format(username))
           # task = st.selectbox("Issue",["Add New Issue","View Issue","Delete Issue"])
           # if task == "Add New Issue":
           #    st.subheader("Create New issue")
           # elif task == "View Issue":
           #    st.subheader("View the issue")
           # elif task == "Delete Issue":
           #    st.subheader("Delet the issue")
           # user_result = view_all_users()
           # clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
           # st.dataframe(clean_db)
        else:
           st.warning("Incorrect Adhar/Passport/VoterID/Password")

    elif choice == "SignUp":
      st.subheader("Create New Account")
      new_user = st.text_input("Adhar/Passport/VoterID")
      new_password = st.text_input("Password",type='password')

      if st.button("Signup"):
        create_usertable(conn)
        add_userdata(conn,new_user,make_hashes(new_password))
        st.success("Account created successfully. Login to application.")

    elif choice == "About":
      st.sidebar.title("App Version details")
      st.sidebar.info("**App version 1.0**")




if __name__ == "__main__":
    main()