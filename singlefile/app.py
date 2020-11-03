import streamlit as st
import pandas as pd
import base64
from PIL import Image
import json

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
    <body style="background-color:red;">
    <div style="background-color:tomato;padding:10px">
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
    menu = ["Home","Login","SignUp","Others","About"]
    st.markdown(
    """
	<style>
	.sidebar .sidebar-content {
	    # background-image: linear-gradient(#264D59, #43978D, #F9E07F, #F9AD6A, #D46C4E);
	    background-image: linear-gradient(to right top, #ebe9f3, #b7bdcc, #8094a5, #496e7c, #0c4950);
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
      inputType = st.sidebar.radio('Radio Button',['Passport','VoterID','Adhar'])

      # Adhar Card will not be having more than 16 digits   
      if inputType == 'Adhar':
      	username = st.sidebar.number_input(inputType+"_No",format='%f')
      	count = len(str(abs(int(username))))
      	if int(count)>int(16):
      		st.sidebar.error('Adhar Card No will not have more than 16 digits. Please enter valid Adhar Card Number.')

      # Passport will not be having more than 8 digits
      elif inputType == 'Passport':
      	username = st.sidebar.text_input(inputType+"_No","DUMMY967")
      	if (username.isalnum()):
      		if (len(username)>int(8)):
      			st.sidebar.error('Passport must be 8 characters long. Please enter valid Passport Number.')
      	else:
      		st.sidebar.error('Passport must be alphanumeric. Please enter valid Passport Number. Eg:- A2345676')

      # VoterID will not be having more than 10 digits
      elif inputType == 'VoterID':
      	username = st.sidebar.text_input(inputType+"_No","DUMMY12345")
      	if (username.isalnum()):
      		if (len(username)>int(10)):
      			st.sidebar.error('VoterID must be 10 characters long. Please enter valid VoterID Number.')
      	else:
      		st.sidebar.error('VoterID must be alphanumeric. Please enter valid VoterID Number. Eg:- A23Y45T676')      	
      	
      password = st.sidebar.text_input("Password",type='password')
    
      if st.sidebar.checkbox("Login"):
        #create_usertable()
        hashed_pswd = make_hashes(password)
        result = login_user(conn,username,check_hashes(password,hashed_pswd))
        if result:
          st.success("Logged In as {0!s}".format(username))
          stateValue = ["Andaman and Nicobar Islands","Andhra Pradesh","Arunachal Pradesh","Assam"]
          distValue=["Alipur","Achampet","Abhayapuri","Along","Adhaura","Central Delhi"]
          areaValue=["value1","value2","value3"]
          partyValue =["None","Congress","BJP","Others"]
          state = st.selectbox("State", stateValue, key="state")
          district = st.selectbox("District", distValue, key="district")
          area = st.selectbox("Area", areaValue, key="area")
          party = st.selectbox("Party", partyValue, key="party")

          vote = st.checkbox('Vote')
          if vote:
          	if party == "Congress":
          		st.write("You have selected/voted to congress! Thanks for voting.")
          		st.balloons()         		

          	elif party == "BJP":
          		st.write("You have selected/voted to BJp! Thanks for voting.")
          		st.balloons()

          	elif party == "Others":
          		st.write("You have selected/voted to Others! Thanks for voting.")
          		st.balloons()

        else:
           st.warning("Incorrect Adhar/Passport/VoterID/Password")

    elif choice == "SignUp":
      st.subheader("Create New Account")
      inputType = st.radio('Radio Button',['Passport','VoterID','Adhar']) 

      # Adhar Card will not be having more than 16 digits   
      if inputType == 'Adhar':
      	new_user = st.number_input(inputType+"_No",format='%f')
      	count = len(str(abs(int(new_user))))
      	if int(count)>int(16):
      		st.error('Adhar Card No will not have more than 16 digits. Please enter valid Adhar Card Number.')

      # Passport will not be having more than 8 digits
      elif inputType == 'Passport':
      	new_user = st.text_input(inputType+"_No","DUMMY967")
      	if (new_user.isalnum()):
      		if (len(new_user)>int(8)):
      			st.error('Passport must be 8 characters long. Please enter valid Passport Number.')
      	else:
      		st.error('Passport must be alphanumeric. Please enter valid Passport Number. Eg:- A2345676')

      # VoterID will not be having more than 10 digits
      elif inputType == 'VoterID':
      	new_user = st.text_input(inputType+"_No","DUMMY12345")
      	if (new_user.isalnum()):
      		if (len(new_user)>int(10)):
      			st.error('VoterID must be 10 characters long. Please enter valid VoterID Number.')
      	else:
      		st.error('VoterID must be alphanumeric. Please enter valid VoterID Number. Eg:- A23Y45T676')      	
      	
      new_password = st.text_input("Password",type='password')

      if st.button("Signup"):
        create_usertable(conn)
        add_userdata(conn,new_user,make_hashes(new_password))
        st.success("Account created successfully. Please Login to application.")

    elif choice == "Others":
    	st.info("Please visit to nearest adhar or passport or voterid location to get any of the ID.")

    elif choice == "About":
      st.sidebar.title("App Version details")
      st.sidebar.info("**App version 1.0**")


if __name__ == "__main__":
    main()