import streamlit as st
import time

from user_functions import login_user

st.title(":rainbow[Home]")

# Initialize login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Initialize username
if "username" not in st.session_state:
    st.session_state.username = ""


if st.session_state.logged_in == False:
    st.subheader("🔐 Login")

    username = st.text_input("Username: ", key = "username")

    password = st.text_input("Password: ", type = "password", key = "password")

    if st.button("Log in", type = "primary"):
            
        if username and password:

            login_successful, login_message = login_user(username, password)
                
            if login_successful:
                st.success(login_message)
                st.session_state.logged_in = True
                st.session_state.username_verified = username
                st.balloons()
                time.sleep(2)
                st.rerun()

            else:
                st.warning(login_message)

        else:
            if not username:          
                st.warning("Please enter a username!")

            if not password:
                st.warning("Please enter a Password!")

if st.session_state.logged_in == True:
    username = st.session_state.username
    st.write(f"Hello, {username}! It's great to see you again!")

    if st.button("Go to the Travel Insurance Calculator"):
        st.switch_page("pages/1_Travel_Insurance_Calculator.py")