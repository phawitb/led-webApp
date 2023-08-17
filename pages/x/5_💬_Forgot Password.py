import streamlit as st
from hash import hash_password,verify_password,load_users,save_users,isEmail
import extra_streamlit_components as stx
import random
from sent_email import sent_otp

st.title("Forgot Password")

if "randomotp" not in st.session_state:
    st.session_state["randomotp"] = False
if "stage_fg" not in st.session_state:
    st.session_state["stage_fg"] = 0
if "email" not in st.session_state:
    st.session_state["email"] = False

if st.session_state["stage_fg"] == 0:
    email = st.text_input("E-mail :")
    if st.button('sent otp'):
        
        if not isEmail(email):
            st.text('not email format')
        elif email not in load_users("users.json"):
            st.text('email not register!!')
        else:
            st.session_state["email"] = email
            st.text('sent otp...')
            otp_sented = str(random.randint(1000,9999))
            st.session_state["randomotp"] = otp_sented 
            if sent_otp(email,st.session_state["randomotp"]):
                st.session_state["stage_fg"] = 1
                st.experimental_rerun()
            else:
                st.text('not sent otp')
                        
elif st.session_state["stage_fg"] == 1:
    otp = st.text_input("OTP :")
    if st.button('comfire otp'):
        if otp == st.session_state["randomotp"]:
            st.session_state["stage_fg"] = 2
            st.experimental_rerun()
        else:
            st.text('incorrect otp')

elif st.session_state["stage_fg"] == 2:
    newpassword = st.text_input("New password :",type="password")
    re_newpassword = st.text_input("Re-New password :", type="password")

    if st.button('confirm'):
        if newpassword == re_newpassword:
            st.text('complete!!')

            users = load_users("users.json")

            username = st.session_state["email"]
            password = newpassword
            hashed_password = hash_password(password)
            users[username] = hashed_password

            save_users("users.json", users)

        else:
            st.text('New password and Re-New password must same value')

