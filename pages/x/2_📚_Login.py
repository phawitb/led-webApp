import streamlit as st
import extra_streamlit_components as stx
from hash import hash_password,verify_password,load_users,save_users,isEmail
import datetime

st.title("Login")

cookie_manager = stx.CookieManager()
person_id = cookie_manager.get(cookie='person_id')

if not person_id:
    
    users = load_users("users.json")
    login_username = st.text_input("Email :")
    login_password = st.text_input("Password :", type="password")

    if not isEmail(login_username):
        st.text("not email format")
    elif login_username not in users:
        st.text("email not register")

    if st.button('LOGIN'):
        if login_username in users:
            if verify_password(users[login_username], login_password):
                st.text("Login successful")
                cookie_manager.set('person_id', login_username, expires_at=datetime.datetime(year=2025, month=2, day=2))
            else:
                st.text("incorrect password")
    
else:
    st.write('current login',person_id)