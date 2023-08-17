import streamlit as st
from sent_email import sent_otp
from hash import hash_password,verify_password,load_users,save_users,isEmail
import random

st.title("Register")

if "sentOTP" not in st.session_state:
    st.session_state["sentOTP"] = False
if "randomotp" not in st.session_state:
    st.session_state["randomotp"] = None
if "email" not in st.session_state:
    st.session_state["email"] = None
if "password" not in st.session_state:
    st.session_state["password"] = None

if not st.session_state["sentOTP"]:
    email = st.text_input("Email :")
    pass1 = st.text_input("Password :",type="password")
    pass2 = st.text_input("Re-Password :",type="password")
    
    if not isEmail(email):
        st.text('not email format')
    elif email in load_users("users.json"):
        st.text('email already register')

    elif pass1 == pass2 and pass1:
        # st.text('password match')
        if st.button("sent otp"):
            st.text('sent otp...')

            otp_sented = str(random.randint(1000,9999))

            st.session_state["randomotp"] = otp_sented 
            if sent_otp(email,st.session_state["randomotp"]):
                st.session_state["email"] = email
                st.session_state["password"] = pass1
                st.session_state["sentOTP"] = True
                st.experimental_rerun()
                        
    else:
        st.text('password unmatch')

else:
    otp = st.text_input("OTP :")
    if st.button("comfirm OTP"):
        if st.session_state["randomotp"] == otp:
            # st.text('OTP match')
            
            users = load_users("users.json")

            username = st.session_state["email"]
            password = st.session_state["password"]
            hashed_password = hash_password(password)
            users[username] = hashed_password

            save_users("users.json", users)

            st.write('Done register',username)

        else:
            st.text('OTP unmatch')


