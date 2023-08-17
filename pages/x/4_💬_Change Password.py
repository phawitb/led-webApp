import streamlit as st
from hash import hash_password,verify_password,load_users,save_users
import extra_streamlit_components as stx

st.title("Change Password")
    
cookie_manager = stx.CookieManager()
person_id = cookie_manager.get(cookie='person_id')

st.text(person_id)

login_password = st.text_input("Old Password :",type="password")
new_passsword = st.text_input("New Password :", type="password")
renew_passsword = st.text_input("Re-New Password :", type="password")

# st.text(login_password)
# st.text(new_passsword)

users = load_users("users.json")

if login_password and verify_password(users[person_id], login_password):
    MATCH = False
    if new_passsword == renew_passsword and new_passsword:
        st.text("match!")
        MATCH = True
        
    else:
        st.text("New Password must same Re-New Password!!")
    if st.button('CONFIRM'):
        if MATCH:
            
            username = person_id
            password = new_passsword
            hashed_password = hash_password(password)
            users[username] = hashed_password

            save_users("users.json", users)

            st.text("Update password compleate!")

else:
    st.text("old password incorrect")

    


