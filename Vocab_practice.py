import streamlit as st
import os, requests, re, time, datetime, json, google.cloud.storage
if not os.path.isfile('key.json'): os.system('wget -O key.json https://storage.googleapis.com/props.davidustranus.space/SAT_VOCAB_TEST.json')
os.system("gcloud auth activate-service-account --key-file='key.json'")
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

########################################################################
#################### HELPER FUNCTIONS ##################################

def create_account_():
	# input user_name
	# validate user_name not in credentials keys
	# input password
	# validate password format
	# upload to datastore # validate success
	# add username:password pair to credentials
	return True, username

st.cache()	
def retrieve_credentials(app_id): 
	# Get all recorded credentials from datastore
	return {}

def password_(username, credentials):
	assert username in credentials.keys(), st.error(f'UserName {username} not recognized')
	credential = credentials[username]
	password = st.sidebar.text_input("Password:", value="")
	# select our text input field and make it into a password input
	js = "el = document.querySelectorAll('.sidebar-content input')[0]; el.type = 'password';"
	# passing js code to the onerror handler of an img tag with no src
	# triggers an error and allows automatically running our code
	html = f'<img src onerror="{js}">'
	# in contrast to st.write, this seems to allow passing javascript
	div = Div(text=html)
	st.bokeh_chart(div)
	if password != credential:
			st.error("the password you entered is incorrect")
	return True




try: credentials 
except: credentials = retrieve_credentials(app_id) ## need to assign app_id

#################### END HELPER FUNCTIONS ##############################
########################################################################
#################### SIDEBAR NAVIGATION ################################

st.header('Login/Create Account') #### User management 
try: 
	assert flag_logged_in == True, ''
	Status = st.text(f'You are logged in. Welcome back {username}')
	log_out = st.button('Log Out')
except:
	Status = st.text('You are NOT logged in')
	try: create_account
	except:
		try: username
		except: username = st.text_input("UserName/Email")
		try: 
			if password == True: 
				Status.text('You are logged in')
				flag_logged_in = True
		except: password = password_()
	create_account = st.button('Create Account')
	if create_account:
		flag_logged_in, username = create_account_()
if log_out:
	lag_logged_in == False		
	
st.write('------------------')

st.header('Navigation') #### Navigation 
try: 
	assert flag_logged_in == True, ''	
	
	Section = st.sidebar.selectbox('App Index',				
																 ('SELECT Vocab set', 			
																	'PRACTICE Vocab set', 
																	'TEST Vocab set'))
																	
if Section == "SELECT Vocab set":
# Retrieve vocab sets
# Multi-select sets


elif	Section == "PRACTICE Vocab set":
# Multi-select level of helps

elif	Section == "TEST Vocab set":
####### display stats summary
	
	
	
except: st.text('Please login to proceed!')
################## END SIDEBAR NAVIGATION ##############################
########################################################################
############################ MAIN BODY #################################
try: 
	assert flag_logged_in == True, ''

if Section == "SELECT Vocab set":


elif	Section == "PRACTICE Vocab set":
	

elif	Section == "TEST Vocab set":	



except: st.text('Please login to proceed!')
######################### END MAIN BODY ################################
########################################################################



