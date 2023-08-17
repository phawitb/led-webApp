import streamlit as st
import extra_streamlit_components as stx

st.title("Logout")

cookie_manager = stx.CookieManager()
person_id = cookie_manager.get(cookie='person_id')

if person_id:
    if st.button('logout'):
        try:
            cookie = 'person_id'
            cookie_manager.delete(cookie)
        except:
            pass
else:
    st.write('no user login')