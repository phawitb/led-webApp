import streamlit as st
import extra_streamlit_components as stx
from hash import hash_password,verify_password,load_users,save_users,isEmail

st.set_page_config(
    page_title="Multipage App",
    page_icon="👋",
)

st.title("Welcome to Login System")


st.write('df',st.session_state["df"])

cookie_manager = stx.CookieManager()
cookies = cookie_manager.get_all()
st.write('cookies',cookies)

users = load_users("users.json")
st.write('All users',list(users.keys()))

person_id = cookie_manager.get(cookie='person_id')
st.write('current user',person_id)

st.sidebar.success(person_id)
# st.sidebar.title('xxxx')



# if "my_input" not in st.session_state:
#     st.session_state["my_input"] = ""

# my_input = st.text_input("Input a text here", st.session_state["my_input"])
# submit = st.button("Submit")
# if submit:
#     st.session_state["my_input"] = my_input
#     st.write("You have entered: ", my_input)